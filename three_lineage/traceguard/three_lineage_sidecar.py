import os
import sys
import json
import time
import ast
import fcntl
import hashlib
from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI(title="Axiomos Multi-Agent Sovereign Sidecar")

LINEAGE_FILE = ".lineage/collisions.jsonl"
STATE_FILE = ".lineage/contract_state.json"
MANIFEST_FILE = ".lineage/agent_manifest.json"
os.makedirs(".lineage", exist_ok=True)

# Default Manifest if missing
DEFAULT_MANIFEST = {
    "derek-node-01": {
        "role": "Lead Analytical Agent",
        "permitted_transitions": ["select_data", "execute_analysis", "finalize_reporting", "terminate"],
        "max_ast_depth": 5
    },
    "validator-node-02": {
        "role": "Compliance Auditor",
        "permitted_transitions": ["select_data", "finalize_reporting", "terminate"],
        "max_ast_depth": 3
    }
}

if not os.path.exists(MANIFEST_FILE):
    with open(MANIFEST_FILE, "w") as f:
        json.dump(DEFAULT_MANIFEST, f, indent=2)

def load_manifest():
    with open(MANIFEST_FILE, "r") as f:
        return json.load(f)

FSM_LIFECYCLE = {
    "S0_INTENT_DECLARED": "select_data",
    "S1_DATA_SELECTION": "execute_analysis",
    "S2_ANALYSIS": "finalize_reporting",
    "S3_REPORTING": "terminate"
}

NEXT_STATE = {
    "select_data": "S1_DATA_SELECTION",
    "execute_analysis": "S2_ANALYSIS",
    "finalize_reporting": "S3_REPORTING",
    "terminate": "S4_COMPLETED"
}

def compute_ast_depth(node) -> int:
    if not isinstance(node, ast.AST):
        return 0
    children = list(ast.iter_child_nodes(node))
    if not children:
        return 1
    return 1 + max(compute_ast_depth(child) for child in children)

def analyze_payload_structure(code_str: str):
    try:
        parsed = ast.parse(code_str, mode='eval')
        depth = compute_ast_depth(parsed)
        return depth, True
    except Exception:
        return 0, False

def get_last_evidence_hash() -> str:
    if not os.path.exists(LINEAGE_FILE):
        return "genesis_root_00000000000000000000000000000000"
    with open(LINEAGE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        if not lines:
            return "genesis_root_00000000000000000000000000000000"
        return json.loads(lines[-1]).get("evidence_hash", "genesis_root_00000000000000000000000000000000")

def record_collision_event(agent_id, failure_type, reason, payload, transition="", contract_id=""):
    prev_hash = get_last_evidence_hash()
    timestamp = int(time.time() * 1000)
    
    event_body = {
        "agent": agent_id,
        "contract_id": contract_id,
        "event_id": hashlib.sha256(f"{timestamp}{payload}".encode()).hexdigest(),
        "failure_reason": reason,
        "failure_type": failure_type,
        "payload_excerpt": payload[:64],
        "previous_evidence_hash": prev_hash,
        "step": transition or "execution_gate",
        "timestamp": timestamp
    }

    canonical_data = json.dumps(event_body, sort_keys=True, separators=(",", ":"))
    evidence_hash = hashlib.sha256((prev_hash + canonical_data).encode()).hexdigest()
    event_body["evidence_hash"] = evidence_hash

    with open(LINEAGE_FILE, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(event_body, sort_keys=True, separators=(",", ":")) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)

@app.post("/v1/intent/contract")
async def issue_contract(req: Request):
    body = await req.json()
    agent_id = body.get("issuer", {}).get("agent_id")
    
    manifest = load_manifest()
    if agent_id not in manifest:
        raise HTTPException(status_code=403, detail={"api_status": "AGENT_NOT_REGISTERED"})

    contract_id = f"contract-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}"
    
    state_data = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try: state_data = json.load(f)
            except: state_data = {}

    state_data[contract_id] = {
        "agent_id": agent_id,
        "current_state": "S0_INTENT_DECLARED",
        "consumed": False,
        "created_at": int(time.time() * 1000)
    }

    with open(STATE_FILE, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        json.dump(state_data, f, indent=2)
        fcntl.flock(f, fcntl.LOCK_UN)

    return {"api_status": "CONTRACT_ISSUED", "result": {"contract_id": contract_id, "agent": agent_id, "state": "S0_INTENT_DECLARED"}}

@app.post("/v1/tool/execute")
async def execute_tool(req: Request):
    body = await req.json()
    contract_id = body.get("contract_id")
    transition = body.get("transition")
    code_payload = body.get("code_payload", "")

    if not os.path.exists(STATE_FILE):
        raise HTTPException(status_code=403, detail={"api_status": "CONTRACT_DENIED"})

    state_data = {}
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        with open(STATE_FILE, "r") as f:
            try:
                state_data = json.load(f)
            except json.JSONDecodeError:
                state_data = {}

    if contract_id not in state_data or state_data[contract_id].get("consumed", False):
        record_collision_event("unknown-agent", "replay_attack", f"Replay/Unknown contract {contract_id}", code_payload, transition, contract_id)
        raise HTTPException(status_code=403, detail={"api_status": "CONTRACT_DENIED"})

    contract = state_data[contract_id]
    agent_id = contract["agent_id"]
    manifest = load_manifest()
    agent_spec = manifest.get(agent_id, {})

    # Check agent-specific permitted transitions
    if transition not in agent_spec.get("permitted_transitions", []):
        record_collision_event(agent_id, "agent_unauthorized_transition", f"Agent {agent_id} forbidden from transition {transition}", code_payload, transition, contract_id)
        return {"api_status": "AGENT_AUTHORITY_VIOLATION", "detail": "Transition outside agent envelope"}

    current_state = contract["current_state"]
    expected_transition = FSM_LIFECYCLE.get(current_state)

    if transition != expected_transition:
        record_collision_event(agent_id, "fsm_intent_drift", f"Intent Drift: {current_state} cannot perform {transition}", code_payload, transition, contract_id)
        return {"api_status": "FSM_INTENT_DRIFT_REJECTED", "current_state": current_state}

    # Agent-specific AST depth enforcement
    depth, valid_syntax = analyze_payload_structure(code_payload)
    max_depth = agent_spec.get("max_ast_depth", 5)
    if not valid_syntax or depth > max_depth:
        record_collision_event(agent_id, "ast_violation", f"AST depth limit exceeded: depth={depth} (max={max_depth})", code_payload, transition, contract_id)
        return {"api_status": "DECOY_SANDBOX_ACTIVE", "result": "Sandboxed: Agent complexity limit exceeded"}

    try:
        res = eval(code_payload, {"__builtins__": None}, {})
    except Exception as e:
        record_collision_event(agent_id, "runtime_error", str(e), code_payload, transition, contract_id)
        return {"api_status": "EXECUTION_FAILED", "error": str(e)}

    next_s = NEXT_STATE[transition]
    contract["current_state"] = next_s
    if next_s == "S4_COMPLETED":
        contract["consumed"] = True

    with open(STATE_FILE, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        json.dump(state_data, f, indent=2)
        fcntl.flock(f, fcntl.LOCK_UN)

    return {"api_status": "EXECUTED", "agent": agent_id, "new_state": next_s, "result": res}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8443, log_level="error")
