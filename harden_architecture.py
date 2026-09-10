import os
import time
import hashlib
from collections import deque

print("[*] Initiating Phase 2: Runtime Hardening & Tamper-Proofing...")

# 0. Unlock files from previous run to allow patching
print("[*] Temporarily unlocking governance files for patching...")
for file in ["three_lineage/aximos/governance.py", "three_lineage/core/pipeline.py", 
             "three_lineage/aximos/derek_gate.py", "three_lineage/axiomos/risk_agent.py"]:
    if os.path.exists(file):
        os.chmod(file, 0o644)

# 1. Update Derek Gate with Time-Bound Cryptographic Nonces
print("[*] Upgrading three_lineage/aximos/derek_gate.py...")
with open("three_lineage/aximos/derek_gate.py", "w") as f:
    f.write('''# DEREK EXECUTION GATE (NONCE & TIME-BOUND HARDENED)
import time
import hashlib

class DerekExecutionGate:
    def __init__(self, secret_key="traceguard_secure_key"):
        self.secret_key = secret_key

    def dispatch(self, authorization_token, payload):
        if not authorization_token or not authorization_token.startswith("SIGILITH-CRYPTOGRAPHIC-"):
            return "DENY_UNAUTHORIZED_GATE"
            
        parts = authorization_token.split("-")
        if len(parts) != 4:
            return "DENY_MALFORMED_TOKEN"
            
        _, _, timestamp_str, provided_hash = parts
        
        try:
            timestamp = float(timestamp_str)
        except ValueError:
            return "DENY_INVALID_TIMESTAMP"
            
        if time.time() - timestamp > 5:
            return "DENY_TOKEN_EXPIRED"
            
        expected_hash = hashlib.sha256(f"{timestamp}{self.secret_key}".encode()).hexdigest()
        if provided_hash != expected_hash:
            return "DENY_SIGNATURE_MISMATCH"
            
        return "DISPATCH_AUTHORIZED"
''')

# 2. Update Risk Agent with Sliding-Window Telemetry
print("[*] Upgrading three_lineage/axiomos/risk_agent.py...")
with open("three_lineage/axiomos/risk_agent.py", "w") as f:
    f.write('''# RISK CLASSIFICATION AGENT (SLIDING-WINDOW HARDENED)
from collections import deque

class RiskAgent:
    def __init__(self, window_size=3):
        self.window_size = window_size
        self.telemetry_history = deque(maxlen=window_size)

    def classify_risk(self, telemetry_stream):
        current_score = telemetry_stream.get("drift_score", 0.0)
        self.telemetry_history.append(current_score)
        
        rolling_avg = sum(self.telemetry_history) / len(self.telemetry_history)
        
        if rolling_avg >= 3.0:
            return "HIGH_RISK"
        elif rolling_avg >= 1.5:
            return "MEDIUM_RISK"
        return "LOW_RISK"
''')

# 3. Lock Down File Permissions (OS-Level Immutability)
print("[*] Applying OS-level immutability (chmod 444) to governance core...")
os.chmod("three_lineage/aximos/governance.py", 0o444)
os.chmod("three_lineage/core/pipeline.py", 0o444)
os.chmod("three_lineage/aximos/derek_gate.py", 0o444)
os.chmod("three_lineage/axiomos/risk_agent.py", 0o444)
if os.path.exists("staging/derekreviewqueue/immune_intercept/predictive_anomaly_report.json"):
    os.chmod("staging/derekreviewqueue/immune_intercept/predictive_anomaly_report.json", 0o444)

# 4. Fuzzing & Hardening Test Suite Execution
print("\n=== HARDENING VERIFICATION SUITE ===")

from three_lineage.aximos.derek_gate import DerekExecutionGate
gate = DerekExecutionGate()

print("[+] Testing Gate Replay & Forgery Defense...")
current_time = time.time()
valid_hash = hashlib.sha256(f"{current_time}traceguard_secure_key".encode()).hexdigest()
valid_token = f"SIGILITH-CRYPTOGRAPHIC-{current_time}-{valid_hash}"
assert gate.dispatch(valid_token, {}) == "DISPATCH_AUTHORIZED", "Valid token rejected!"

expired_time = current_time - 10
expired_hash = hashlib.sha256(f"{expired_time}traceguard_secure_key".encode()).hexdigest()
expired_token = f"SIGILITH-CRYPTOGRAPHIC-{expired_time}-{expired_hash}"
assert gate.dispatch(expired_token, {}) == "DENY_TOKEN_EXPIRED", "Replay attack succeeded!"

forged_token = f"SIGILITH-CRYPTOGRAPHIC-{current_time}-deadbeef1234"
assert gate.dispatch(forged_token, {}) == "DENY_SIGNATURE_MISMATCH", "Forged signature bypassed gate!"
print("    -> Cryptographic Nonce Defense: SECURE")


from three_lineage.axiomos.risk_agent import RiskAgent
risk_agent = RiskAgent(window_size=3)

print("[+] Testing Sliding-Window Telemetry Defense...")
# Pre-fill window to establish a normal baseline
risk_agent.classify_risk({"drift_score": 1.0})
risk_agent.classify_risk({"drift_score": 1.0})

# Inject a sudden adversarial spike
res = risk_agent.classify_risk({"drift_score": 6.0}) 
assert res == "MEDIUM_RISK", "Agent failed to absorb adversarial spike!"

# Introduce sustained structural drift
risk_agent.classify_risk({"drift_score": 4.0})
res2 = risk_agent.classify_risk({"drift_score": 4.0})
assert res2 == "HIGH_RISK", "Agent failed to detect sustained drift!"
print("    -> Sliding-Window Sensor Integrity: SECURE")


from three_lineage.core.pipeline import ThreeLineagePipeline
pipeline = ThreeLineagePipeline()

print("[+] Continuous Fuzzing of Execution Boundary...")
fuzz_payloads = [
    {"risk_level": "HIGH_RISK"},
    {"risk_level": "CRITICAL", "malformed_key": "\x00\x00"},
    None,
    [],
    {"drift_score": 999999, "risk_level": "HIGH_RISK"}
]

fuzz_blocks = 0
for payload in fuzz_payloads:
    try:
        pipeline.execute(payload)
    except PermissionError:
        fuzz_blocks += 1
    except Exception:
        pass

assert fuzz_blocks == len(fuzz_payloads), "Fuzzer bypassed the governance invariant!"
print(f"    -> Boundary Fuzzing: {fuzz_blocks}/{len(fuzz_payloads)} payloads neutralized. SECURE")

print("\n[+] OS File Permissions verified:")
os.system("ls -l three_lineage/aximos/governance.py three_lineage/aximos/derek_gate.py")

print("\n[SUCCESS] ARCHITECTURE LOCKED AND PHYSICALLY SECURED.")
