from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from traceguard.traceguard import TraceGuard
from traceguard.asyncledger import AsyncEvidenceLedger
from traceguard.aximos import AXIOMOSEvaluator

app = FastAPI(title="TraceGuard Secured Agent Gateway")

governance_engine = TraceGuard(allowed_actions=["read_logs", "safe_query", "generate_report"])
audit_ledger = AsyncEvidenceLedger()
risk_evaluator = AXIOMOSEvaluator(block_threshold=2)

class AgentActionRequest(BaseModel):
    agent_id: str
    action_name: str
    payload: dict

@app.post("/v1/agent/execute")
async def execute_agent_action(request: AgentActionRequest):
    decision = governance_engine.evaluate_action(request.action_name)
    
    log_entry = await audit_ledger.append_entry({
        "agent_id": request.agent_id,
        "action": request.action_name,
        "payload": request.payload,
        "decision": decision
    })
    
    current_risk = risk_evaluator.evaluate_logs(audit_ledger.chain)
    
    if decision == "BLOCK" or current_risk == "HIGH_RISK":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "TraceGuard Zero-Trust Containment Triggered",
                "decision": decision,
                "axiomos_risk": current_risk,
                "provenance_hash": log_entry["current_hash"]
            }
        )
        
    return {
        "status": "APPROVED",
        "provenance_hash": log_entry["current_hash"],
        "axiomos_risk": current_risk
    }

@app.get("/v1/audit/verify")
async def verify_ledger_integrity():
    is_valid = await audit_ledger.verify_integrity()
    return {
        "chain_length": len(audit_ledger.chain),
        "cryptographic_integrity_verified": is_valid,
        "head_hash": audit_ledger.chain[-1]["current_hash"] if audit_ledger.chain else None
    }
