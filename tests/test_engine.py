from src.traceguard import TraceGuard
from src.aximos import AXIOMOSEvaluator
from src.matrix import AssuranceMatrix

def test_traceguard_allow_block():
    tg = TraceGuard(allowed_actions=["read"])
    assert tg.evaluate_action("read") == "ALLOW"
    assert tg.evaluate_action("write") == "BLOCK"

def test_aximos_risk():
    ax = AXIOMOSEvaluator(block_threshold=1)
    logs = [{"decision": "BLOCK"}]
    assert ax.evaluate_logs(logs) == "HIGH_RISK"

def test_assurance_matrix():
    matrix = AssuranceMatrix()
    res = matrix.calculate_tier(consequence=1, autonomy=1, oversight=True)
    assert "Tier" in res["tier"]
