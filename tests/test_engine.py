import pytest
from traceguard import TraceGuard, AXIOMOSEvaluator

def test_traceguard_allowed_action():
    guard = TraceGuard(allowed_actions=["read_logs"])
    assert guard.evaluate_action("read_logs") == "ALLOW"

def test_traceguard_unauthorized_block():
    guard = TraceGuard(allowed_actions=["read_logs"])
    assert guard.evaluate_action("drop_tables") == "BLOCK"

def test_traceguard_malformed_request():
    guard = TraceGuard(allowed_actions=["read_logs"])
    assert guard.evaluate_action("") == "BLOCK"

def test_traceguard_repeated_breach_persistence():
    guard = TraceGuard(allowed_actions=["read_logs"])
    guard.evaluate_action("unauthorized_1")
    guard.evaluate_action("unauthorized_2")
    assert guard.get_breach_count() == 2

def test_aximos_risk_fixtures():
    evaluator = AXIOMOSEvaluator()
    dummy_chain = [{"payload": {"decision": "BLOCK"}}, {"payload": {"decision": "BLOCK"}}]
    tier = evaluator.evaluate_logs(dummy_chain)
    assert tier in ["LOW_RISK", "NOMINAL", "ELEVATED_THREAT", "HIGH_RISK_CONTAINMENT"]

def test_assurance_matrix():
    evaluator = AXIOMOSEvaluator(block_threshold=1)
    dummy_chain = [{"payload": {"decision": "BLOCK"}}]
    tier = evaluator.evaluate_logs(dummy_chain)
    assert tier in ["LOW_RISK", "HIGH_RISK_CONTAINMENT"]
