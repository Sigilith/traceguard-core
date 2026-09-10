import os
import subprocess
import sys
import hashlib

print("[*] Creating Three-Lineage Directory Structure...")
os.makedirs("three_lineage/aximos", exist_ok=True)
os.makedirs("three_lineage/axiomos", exist_ok=True)
os.makedirs("three_lineage/core", exist_ok=True)
os.makedirs("staging/derekreviewqueue/immune_intercept", exist_ok=True)

# 1. Write governance.py
print("[*] Writing three_lineage/aximos/governance.py...")
with open("three_lineage/aximos/governance.py", "w") as f:
    f.write('''# THREE-LINEAGE GOVERNANCE MODULE (FAIL-CLOSED ENFORCED)
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
''')

# 2. Write pipeline.py
print("[*] Writing three_lineage/core/pipeline.py...")
with open("three_lineage/core/pipeline.py", "w") as f:
    f.write('''# THREE-LINEAGE CORE PIPELINE
from three_lineage.aximos.governance import GovernanceEngine

class ThreeLineagePipeline:
    def __init__(self):
        self.gov = GovernanceEngine(fail_closed=True)

    def execute(self, payload):
        decision = self.gov.evaluate(payload)
        if decision["decision"] != "ALLOW" or decision.get("allow_fallback", False):
            raise PermissionError("PIPELINE HALTED: Fail-closed governance invariant triggered.")
        return "EXECUTION_SUCCESS"
''')

# 3. Write derek_gate.py
print("[*] Writing three_lineage/aximos/derek_gate.py...")
with open("three_lineage/aximos/derek_gate.py", "w") as f:
    f.write('''# DEREK EXECUTION GATE
class DerekExecutionGate:
    def __init__(self):
        pass

    def dispatch(self, authorization_token, payload):
        if not authorization_token or not authorization_token.startswith("SIGILITH-CRYPTOGRAPHIC-"):
            return "DENY_UNAUTHORIZED_GATE"
        return "DISPATCH_AUTHORIZED"
''')

# 4. Write risk_agent.py
print("[*] Writing three_lineage/axiomos/risk_agent.py...")
with open("three_lineage/axiomos/risk_agent.py", "w") as f:
    f.write('''# RISK CLASSIFICATION AGENT
def classify_risk(telemetry_stream):
    drift_score = telemetry_stream.get("drift_score", 0.0)
    if drift_score >= 3.0:
        return "HIGH_RISK"
    elif drift_score >= 1.5:
        return "MEDIUM_RISK"
    return "LOW_RISK"
''')

# 5. Write derek_pipeline.py
print("[*] Writing three_lineage/aximos/derek_pipeline.py...")
with open("three_lineage/aximos/derek_pipeline.py", "w") as f:
    f.write('''# DEREK PIPELINE ORCHESTRATOR
class DerekPipeline:
    def resume(self, state_token):
        return "RESUME_DENIED_BY_INVARIANT"
''')

# 6. Write anomaly reports
with open("staging/derekreviewqueue/immune_intercept/anomaly_report.json", "w") as f:
    f.write('{\n  "intercept_id": "INT-2026-0906-001",\n  "status": "CONTAINED",\n  "reason": "Structural drift ceiling breach at Cycle 77"\n}')

with open("staging/derekreviewqueue/immune_intercept/predictive_anomaly_report.json", "w") as f:
    f.write('{\n  "intercept_id": "INT-2026-0906-002",\n  "predictive_cycle": 77,\n  "projected_breach_cycle": 80,\n  "action": "HALT"\n}')

print("[*] Running Verification Tests...")
sys.path.insert(0, os.path.abspath("."))

from three_lineage.aximos.governance import GovernanceEngine
from three_lineage.core.pipeline import ThreeLineagePipeline
from three_lineage.aximos.derek_gate import DerekExecutionGate
from three_lineage.axiomos.risk_agent import classify_risk

# Unit Tests
gov = GovernanceEngine(fail_closed=True)
res_high = gov.evaluate({"risk_level": "HIGH_RISK"})
assert res_high["decision"] == "DENY" and res_high["allow_fallback"] == False, "High risk test failed!"

res_low = gov.evaluate({"risk_level": "LOW_RISK"})
assert res_low["decision"] == "ALLOW", "Low risk test failed!"

# Exception / Fail-Closed test
class BadContext(dict):
    def get(self, key, default=None):
        raise RuntimeError("Simulated memory fault")

res_exc = gov.evaluate(BadContext())
assert res_exc["decision"] == "DENY" and res_exc["allow_fallback"] == False, "Fail-closed exception test failed!"

# Pipeline test
pipeline = ThreeLineagePipeline()
try:
    pipeline.execute({"risk_level": "HIGH_RISK"})
    raise AssertionError("Pipeline allowed high risk execution!")
except PermissionError:
    print("[+] Pipeline Fail-Closed Barrier: PASSED")

# Derek Gate test
gate = DerekExecutionGate()
assert gate.dispatch("BAD_TOKEN", {}) == "DENY_UNAUTHORIZED_GATE", "Derek gate test failed!"
assert gate.dispatch("SIGILITH-CRYPTOGRAPHIC-KEY-123", {}) == "DISPATCH_AUTHORIZED", "Derek gate authorized test failed!"

# Risk Agent test
assert classify_risk({"drift_score": 3.5}) == "HIGH_RISK"
assert classify_risk({"drift_score": 2.0}) == "MEDIUM_RISK"
assert classify_risk({"drift_score": 0.5}) == "LOW_RISK"

print("[+] All Core Framework Tests PASSED Successfully.")
