from axiomos.policy import PolicyEngine
from typing import Dict, Any

class LineageGovernanceAdapter:
    """Thin adapter binding Three-Lineage telemetry pipeline to AXIOMOS v2.2.1 PolicyEngine."""
    
    def __init__(self):
        self.engine = PolicyEngine()

    def evaluate(self, event_type: str, meta: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates runtime events against AXIOMOS governance policies."""
        signal = {
            "event_type": event_type,
            **meta
        }
        decision = self.engine.govern(signal)
        
        return {
            "decision": decision.decision,
            "priority": decision.priority,
            "authority": decision.authority,
            "policy_id": decision.policy_id,
            "policy_name": decision.policy_name,
            "recommended_action": decision.recommended_action,
            "reasoning": decision.reasoning,
            "release_response": decision.release_response
        }

    def govern_telemetry(self, telemetry_sample: float) -> Dict[str, Any]:
        """Legacy helper for numeric telemetry samples."""
        return self.evaluate("telemetry", {"telemetry_sample": telemetry_sample})
