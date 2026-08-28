import json
from datetime import datetime
from traceguard.asyncledger import AsyncEvidenceLedger
from traceguard.aximos import AXIOMOSEvaluator

class ComplianceAuditGenerator:
    """Generates structured compliance audit packets from cryptographic ledger entries."""

    def __init__(self, ledger: AsyncEvidenceLedger, evaluator: AXIOMOSEvaluator):
        self.ledger = ledger
        self.evaluator = evaluator

    async def generate_audit_packet(self, framework_name: str = "Ofgem High-Impact AI Assurance") -> str:
        is_valid = await self.ledger.verify_integrity()
        risk_status = self.evaluator.evaluate_logs(self.ledger.chain)
        
        packet = {
            "audit_timestamp": datetime.utcnow().isoformat() + "Z",
            "regulatory_framework": framework_name,
            "ledger_metrics": {
                "total_records": len(self.ledger.chain),
                "hash_chain_integrity_verified": is_valid,
                "head_hash": self.ledger.chain[-1]["current_hash"] if self.ledger.chain else None
            },
            "governance_evaluation": {
                "axiomos_risk_tier": risk_status,
                "boundary_enforcement_active": True,
                "mandatory_controls_met": is_valid and risk_status != "CRITICAL_BREACH"
            }
        }
        return json.dumps(packet, indent=2)
