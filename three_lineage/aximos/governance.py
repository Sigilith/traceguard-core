# THREE-LINEAGE GOVERNANCE MODULE (FAIL-CLOSED ENFORCED)
import logging

logger = logging.getLogger("ThreeLineage.Governance")

class GovernanceEngine:
    def __init__(self, fail_closed=True):
        self.fail_closed = fail_closed

    def evaluate(self, context):
        try:
            risk_level = context.get("risk_level", "HIGH_RISK")
            if risk_level in ["HIGH_RISK", "CRITICAL"]:
                logger.warning("Governance ceiling breached. Enforcing DENY.")
                return {"decision": "DENY", "allow_fallback": False}
            return {"decision": "ALLOW", "allow_fallback": False}
        except Exception as e:
            logger.error(f"Governance exception encountered: {e}. Defaulting to fail-closed.")
            if self.fail_closed:
                return {"decision": "DENY", "allow_fallback": False}
            else:
                return {"decision": "ALLOW", "allow_fallback": True}
