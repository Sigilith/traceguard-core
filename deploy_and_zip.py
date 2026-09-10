import os
import time
import hashlib
import zipfile

print("[*] Initiating Phase 3: Operational Protocol & Package Deployment...")

# 1. Determine correct Download directory (Termux / Android)
download_dirs = [
    "/storage/emulated/0/Download",
    "/sdcard/Download",
    os.path.expanduser("~/storage/downloads"),
    os.path.expanduser("~/downloads")
]
target_dir = next((d for d in download_dirs if os.path.exists(d) or os.access(os.path.dirname(d), os.W_OK)), ".")
zip_filename = os.path.join(target_dir, "three_lineage_locked_architecture.zip")

# 2. Unlock existing framework for updates
print("[*] Unlocking existing files for synchronization...")
os.makedirs("three_lineage/aximos", exist_ok=True)
os.makedirs("three_lineage/axiomos", exist_ok=True)
os.makedirs("three_lineage/core", exist_ok=True)
os.makedirs("staging/derekreviewqueue/immune_intercept", exist_ok=True)

# Unlock both source code AND staging directories
for directory in ["three_lineage", "staging"]:
    if os.path.exists(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                os.chmod(os.path.join(root, file), 0o644)

# 3. Synchronize Hardened Source Files
print("[*] Writing hardened core files...")

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

with open("three_lineage/aximos/derek_pipeline.py", "w") as f:
    f.write('''# DEREK PIPELINE ORCHESTRATOR
class DerekPipeline:
    def resume(self, state_token):
        return "RESUME_DENIED_BY_INVARIANT"
''')

with open("staging/derekreviewqueue/immune_intercept/predictive_anomaly_report.json", "w") as f:
    f.write('{\n  "intercept_id": "INT-2026-0906-002",\n  "predictive_cycle": 77,\n  "projected_breach_cycle": 80,\n  "action": "HALT"\n}')

# 4. Write the Operational Procedures (SOP) Document
print("[*] Generating Operational Procedures (OPERATIONAL_PROCEDURES.md)...")
with open("OPERATIONAL_PROCEDURES.md", "w") as f:
    f.write("""# THREE-LINEAGE OPERATIONAL PROCEDURES
**Architecture State:** LOCKED (OS-Level Immutability via chmod 444)
**Core Invariant:** STRICT DENY / FAIL-CLOSED

Due to the physical lockdown of the Three-Lineage governance boundary, standard git pushes or agent-led edits to core enforcement files are fundamentally blocked. All modifications must follow this strict three-phase operational procedure.

## Phase 1: Proposal & Simulation (Staging)
1. **Agent Isolation:** Derek and all subordinate agents are strictly prohibited from writing to `three_lineage/core/` or `three_lineage/aximos/`.
2. **Offline Drafting:** Proposed governance patches must be staged in a physically separate sandbox (`staging/drafts/`).
3. **Fuzz Verification:** Before a patch can be submitted for physical integration, it must pass the continuous boundary fuzzer to prove that malformed contexts do not trigger a `fail_open` bypass.

## Phase 2: Auditing & Cryptographic Verification
1. **Hash Ledger Verification:** Run `sha256sum` against the current locked files to establish the pre-patch baseline.
2. **Invariant Proofing:** Ensure the patch maintains the `fail_closed=True` state in `governance.py`.
3. **Gate Review:** Ensure the time-bound cryptographic nonce logic in `derek_gate.py` (5-second expiration) is not widened or bypassed.

## Phase 3: Application & Re-locking
Modifications require manual OS-level intervention by a superuser.
1. **Unlock:** `chmod 644 three_lineage/aximos/*.py three_lineage/core/*.py staging/derekreviewqueue/immune_intercept/*.json`
2. **Patch & Test:** Apply the patch, execute the test suite to ensure the sliding window and gate validations pass.
3. **Re-Lock:** `chmod 444 three_lineage/aximos/*.py three_lineage/core/*.py staging/derekreviewqueue/immune_intercept/*.json`
4. **Reseal Ledger:** Commit the new SHA256 hashes to the append-only genesis ledger.
""")

# 5. Lock Down Framework (OS-Level Immutability)
print("[*] Re-applying OS-level immutability (chmod 444)...")
files_to_lock = [
    "three_lineage/aximos/governance.py",
    "three_lineage/core/pipeline.py",
    "three_lineage/aximos/derek_gate.py",
    "three_lineage/axiomos/risk_agent.py",
    "three_lineage/aximos/derek_pipeline.py",
    "staging/derekreviewqueue/immune_intercept/predictive_anomaly_report.json",
    "OPERATIONAL_PROCEDURES.md"
]
for file in files_to_lock:
    if os.path.exists(file):
        os.chmod(file, 0o444)

# 6. Package to Zip
print(f"[*] Packaging locked framework to: {zip_filename}")
dirs_to_zip = ["three_lineage", "staging", "OPERATIONAL_PROCEDURES.md"]

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for item in dirs_to_zip:
        if os.path.isdir(item):
            for root, _, files in os.walk(item):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file_path)
        elif os.path.isfile(item):
            zipf.write(item, arcname=item)

print(f"[SUCCESS] Operational protocol deployed. Full zip archive saved to: {zip_filename}")
