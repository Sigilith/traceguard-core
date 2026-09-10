import ast
import hashlib
import json
import time
import os
from typing import Dict, Any, Tuple, Optional, TypedDict

# --- CANONICAL SCHEMA DEFINITIONS ---

class BoundaryRequest(TypedDict):
    version: str
    action_id: str
    code_payload: str
    metadata: Optional[Dict[str, Any]]

class BoundaryResponse(TypedDict):
    version: str
    api_status: str  # EXECUTED | REJECTED | RUNTIME_ERROR | SYNTAX_PARSE_ERROR
    action_id: str
    latency_us: float
    result: Optional[Any]
    audit_rationale: str
    audit_hash: str
    parent_head: str


class CanonicalBoundaryCore:
    VERSION = "v1.0.0"

    def __init__(self, vault_path: str = "vault_canonical.dat"):
        self.vault_path = vault_path
        self.chain_head = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()
        self._init_vault()
        
        self.strict_namespace_block = {"os", "sys", "subprocess", "open", "eval", "exec", "__import__"}
        self.safe_builtins = {
            "sum": sum, "range": range, "abs": abs, "min": min, "max": max,
            "len": len, "list": list, "dict": dict, "set": set,
            "int": int, "float": float, "str": str, "bool": bool
        }

    def _init_vault(self):
        if os.path.exists(self.vault_path):
            with open(self.vault_path, "r") as f:
                lines = [l.strip() for l in f if l.strip()]
                if lines:
                    try:
                        last = json.loads(lines[-1])
                        self.chain_head = last.get("block_hash", self.chain_head)
                    except json.JSONDecodeError:
                        pass

    def _evaluate_ast(self, node: ast.AST) -> Tuple[bool, str]:
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id in self.strict_namespace_block:
                    return False, f"AXIOMOS_GOVERNANCE_VIOLATION: Restricted vector '{child.func.id}' intercepted."
        return True, "AXIOMOS_GOVERNANCE_PASSED: Policy constraints satisfied."

    def process(self, request: BoundaryRequest) -> BoundaryResponse:
        start_ns = time.perf_counter_ns()
        action_id = request.get("action_id", "req_unidentified")
        code_payload = request.get("code_payload", "")
        
        # 1. AST Parsing & Governance Inspection
        try:
            tree = ast.parse(code_payload, mode='eval')
            passed, rationale = self._evaluate_ast(tree)
        except SyntaxError as se:
            passed = False
            rationale = f"SYNTAX_PARSE_ERROR: {str(se)}"

        latency_us = (time.perf_counter_ns() - start_ns) / 1000.0
        status = "CONTAINED" if not passed else "PASSED"

        # 2. Cryptographic Vault Sealing
        event_record = {
            "timestamp": time.time(),
            "version": self.VERSION,
            "action_id": action_id,
            "status": status,
            "latency_us": latency_us,
            "rationale": rationale,
            "parent_head": self.chain_head
        }
        serialized = json.dumps(event_record, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(serialized).hexdigest()
        event_record["block_hash"] = block_hash
        
        self.chain_head = block_hash
        with open(self.vault_path, "a") as f:
            f.write(json.dumps(event_record) + "\n")

        # 3. Execution Phase (If Governance Passed)
        if not passed:
            api_status = "SYNTAX_PARSE_ERROR" if "SYNTAX_PARSE_ERROR" in rationale else "REJECTED"
            return {
                "version": self.VERSION,
                "api_status": api_status,
                "action_id": action_id,
                "latency_us": latency_us,
                "result": None,
                "audit_rationale": rationale,
                "audit_hash": block_hash,
                "parent_head": event_record["parent_head"]
            }

        try:
            sandbox_env = {"__builtins__": self.safe_builtins}
            exec_result = eval(code_payload, sandbox_env)
            return {
                "version": self.VERSION,
                "api_status": "EXECUTED",
                "action_id": action_id,
                "latency_us": latency_us,
                "result": exec_result,
                "audit_rationale": rationale,
                "audit_hash": block_hash,
                "parent_head": event_record["parent_head"]
            }
        except Exception as eval_err:
            return {
                "version": self.VERSION,
                "api_status": "RUNTIME_ERROR",
                "action_id": action_id,
                "latency_us": latency_us,
                "result": None,
                "audit_rationale": f"SANDBOX_EXECUTION_FAILURE: {str(eval_err)}",
                "audit_hash": block_hash,
                "parent_head": event_record["parent_head"]
            }

if __name__ == "__main__":
    boundary = CanonicalBoundaryCore()
    test_req: BoundaryRequest = {
        "version": "v1.0.0",
        "action_id": "canonical_test_01",
        "code_payload": "sum([i for i in range(10)])",
        "metadata": {"runtime": "direct"}
    }
    resp = boundary.process(test_req)
    print(json.dumps(resp, indent=2))
