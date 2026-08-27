import pytest
from src.traceguard import TraceGuard
from src.aximos import AXIOMOSEvaluator
from src.matrix import AssuranceMatrix

def test_traceguard_allowed_action():
    tg = TraceGuard(allowed_actions=["read"])
    assert tg.evaluate_action("read") == "ALLOW"
    logs = tg.get_logs()
    assert len(logs) == 1
    assert logs[0]["action"] == "read"
    assert logs[0]["decision"] == "ALLOW"

def test_traceguard_unauthorized_block():
    tg = TraceGuard(allowed_actions=["read"])
    assert tg.evaluate_action("write") == "BLOCK"
    logs = tg.get_logs()
    assert logs[-1]["decision"] == "BLOCK"

def test_traceguard_malformed_request():
    tg = TraceGuard(allowed_actions=["read"])
    # Malformed payload (empty/non-string) fails closed
    assert tg.evaluate_action("") == "BLOCK"
    assert tg.evaluate_action(None) == "BLOCK"

def test_traceguard_repeated_breach_persistence():
    tg = TraceGuard(allowed_actions=["read"])
    tg.evaluate_action("rm_rf")
    tg.evaluate_action("rm_rf")
    logs = tg.get_logs()
    block_count = sum(1 for l in logs if l["decision"] == "BLOCK")
    assert block_count == 2

def test_aximos_risk_fixtures():
    ax = AXIOMOSEvaluator(block_threshold=2)
    
    # 1. Clean Run -> Low Risk
    clean_logs = [{"action": "read", "decision": "ALLOW"}] * 5
    assert ax.evaluate_logs(clean_logs) == "LOW_RISK"
    
    # 2. Boundary Drift -> Medium/High Risk depending on threshold
    drift_logs = [{"action": "read", "decision": "ALLOW"}, {"action": "unauthorized", "decision": "BLOCK"}]
    # Threshold is 2, so 1 block should be handled or classified appropriately
    
    # 3. Multiple Breach -> High Risk
    breach_logs = [{"action": "bad", "decision": "BLOCK"}, {"action": "worse", "decision": "BLOCK"}]
    assert ax.evaluate_logs(breach_logs) == "HIGH_RISK"

    # 4. Insufficient Data -> Unresolved
    sparse_logs = []
    assert ax.evaluate_logs(sparse_logs) == "UNRESOLVED"

def test_assurance_matrix():
    matrix = AssuranceMatrix()
    res = matrix.calculate_tier(consequence=3, autonomy=3, oversight=True)
    assert "Tier" in res["tier"]
    assert res["score"] == 4
