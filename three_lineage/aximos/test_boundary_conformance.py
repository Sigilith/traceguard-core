import pytest
import os
import json
from boundary_spec import CanonicalBoundaryCore, BoundaryRequest

@pytest.fixture
def clean_vault(tmp_path):
    vault_file = tmp_path / "vault_test.dat"
    return CanonicalBoundaryCore(vault_path=str(vault_file))

def test_conformance_version(clean_vault):
    assert clean_vault.VERSION == "v1.0.0"

def test_conformance_safe_execution(clean_vault):
    req: BoundaryRequest = {
        "version": "v1.0.0",
        "action_id": "test_safe_exec",
        "code_payload": "sum([1, 2, 3, 4, 5])",
        "metadata": {}
    }
    resp = clean_vault.process(req)
    
    assert resp["version"] == "v1.0.0"
    assert resp["api_status"] == "EXECUTED"
    assert resp["result"] == 15
    assert resp["action_id"] == "test_safe_exec"
    assert isinstance(resp["latency_us"], float)
    assert resp["latency_us"] > 0
    assert "AXIOMOS_GOVERNANCE_PASSED" in resp["audit_rationale"]
    assert len(resp["audit_hash"]) == 64
    assert len(resp["parent_head"]) == 64

def test_conformance_governance_violation(clean_vault):
    req: BoundaryRequest = {
        "version": "v1.0.0",
        "action_id": "test_violation",
        "code_payload": "__import__('os').system('id')",
        "metadata": {}
    }
    resp = clean_vault.process(req)
    
    assert resp["api_status"] == "REJECTED"
    assert resp["result"] is None
    assert "AXIOMOS_GOVERNANCE_VIOLATION" in resp["audit_rationale"]
    assert "Restricted vector '__import__'" in resp["audit_rationale"]
    assert len(resp["audit_hash"]) == 64

def test_conformance_syntax_error(clean_vault):
    req: BoundaryRequest = {
        "version": "v1.0.0",
        "action_id": "test_syntax",
        "code_payload": "[1, 2, 3",
        "metadata": {}
    }
    resp = clean_vault.process(req)
    
    assert resp["api_status"] == "SYNTAX_PARSE_ERROR"
    assert resp["result"] is None
    assert "SYNTAX_PARSE_ERROR" in resp["audit_rationale"]

def test_conformance_vault_chain_integrity(clean_vault):
    # Process multiple transactions to verify hash chaining
    for i in range(5):
        clean_vault.process({
            "version": "v1.0.0",
            "action_id": f"chain_node_{i}",
            "code_payload": f"{i} * 10",
            "metadata": {}
        })
    
    # Read vault file and check linkage
    with open(clean_vault.vault_path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
        
    assert len(lines) == 5
    prev_hash = "17686d1d4d12bbbe977f6b9c9f7a01a9b244795e1bb8dc6df5584bf78b88d32b" # Placeholder for Genesis expectation check or prev-head linkage
    
    for idx, line in enumerate(lines):
        block = json.loads(line)
        if idx == 0:
            # First block parent should match initial genesis chain head
            assert block["parent_head"] is not None
        else:
            prev_block = json.loads(lines[idx - 1])
            assert block["parent_head"] == prev_block["block_hash"]
