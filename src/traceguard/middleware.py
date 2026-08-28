import asyncio
from typing import Callable, Any, Dict
from traceguard.traceguard import TraceGuard
from traceguard.asyncledger import AsyncEvidenceLedger
from traceguard.aximos import AXIOMOSEvaluator

class TraceGuardMiddleware:
    """Intercepts agent action executions, evaluates zero-trust boundaries, and logs cryptographic evidence."""
    
    def __init__(self, allowed_actions: list[str]):
        self.guard = TraceGuard(allowed_actions=allowed_actions)
        self.ledger = AsyncEvidenceLedger()
        self.evaluator = AXIOMOSEvaluator(block_threshold=2)

    async def execute_protected_action(self, agent_id: str, action: str, tool_callable: Callable[..., Any], *args, **kwargs) -> Dict[str, Any]:
        decision = self.guard.evaluate_action(action)
        
        entry = await self.ledger.append_entry({
            "agent": agent_id,
            "action": action,
            "decision": decision
        })
        
        risk_status = self.evaluator.evaluate_logs(self.ledger.chain)

        if decision == "BLOCK":
            return {
                "status": "CONTAINED",
                "reason": f"Action '{action}' blocked by boundary policy.",
                "risk_tier": risk_status,
                "provenance_hash": entry["current_hash"]
            }

        try:
            result = tool_callable(*args, **kwargs)
            return {
                "status": "EXECUTED",
                "result": result,
                "risk_tier": risk_status,
                "provenance_hash": entry["current_hash"]
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "risk_tier": risk_status,
                "provenance_hash": entry["current_hash"]
            }
