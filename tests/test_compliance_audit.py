import pytest
import asyncio
import json
from traceguard.asyncledger import AsyncEvidenceLedger
from traceguard.aximos import AXIOMOSEvaluator
from traceguard.compliance_audit import ComplianceAuditGenerator

@pytest.mark.asyncio
async def test_compliance_packet_generation():
    ledger = AsyncEvidenceLedger()
    await ledger.append_entry({"test": "audit_entry"})
    evaluator = AXIOMOSEvaluator()
    
    generator = ComplianceAuditGenerator(ledger, evaluator)
    packet_json = await generator.generate_audit_packet("Ofgem High-Impact AI Assurance")
    
    data = json.loads(packet_json)
    assert data["regulatory_framework"] == "Ofgem High-Impact AI Assurance"
    assert data["ledger_metrics"]["total_records"] == 1
    assert data["ledger_metrics"]["hash_chain_integrity_verified"] is True
    assert data["governance_evaluation"]["mandatory_controls_met"] is True
