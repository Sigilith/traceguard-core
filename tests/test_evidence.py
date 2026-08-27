import pytest
from src.evidence import EvidenceLedger

def test_ledger_integrity_valid():
    ledger = EvidenceLedger()
    ledger.append_entry({"action": "safe_query", "decision": "ALLOW"})
    ledger.append_entry({"action": "unauthorized_exec", "decision": "BLOCK"})
    
    assert ledger.verify_integrity() is True

def test_ledger_tamper_detection():
    ledger = EvidenceLedger()
    ledger.append_entry({"action": "safe_query", "decision": "ALLOW"})
    ledger.append_entry({"action": "unauthorized_exec", "decision": "BLOCK"})
    
    assert ledger.verify_integrity() is True
    
    ledger.tamper_with_entry(0, {"action": "safe_query", "decision": "BLOCK_BYPASSED"})
    
    assert ledger.verify_integrity() is False
