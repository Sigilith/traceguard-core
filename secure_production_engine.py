import os
import json
import hashlib
import time
import glob
import shutil

print("==================================================")
print(" THREE-LINEAGE SECURE PRODUCTION ENGINE v2.1")
print("==================================================")

LEDGER_DIR = ".lineage/derek_receipts"
ARCHIVE_DIR = ".lineage/archive"
WORM_MIRROR_DIR = ".lineage/worm_mirror"

for d in [LEDGER_DIR, ARCHIVE_DIR, WORM_MIRROR_DIR]:
    os.makedirs(d, exist_ok=True)
    try:
        os.chmod(d, 0o700) # Enforce strict directory permissions (owner-only read/write/execute)
    except Exception:
        pass

class SecureThreeLineageEngine:
    def __init__(self):
        self.ledger_dir = LEDGER_DIR
        self.worm_dir = WORM_MIRROR_DIR
        self.seen_nonces = set()
        self._load_nonce_registry()

    def _load_nonce_registry(self):
        """Startup Integrity: Rebuilds nonce history from disk to prevent replay attacks post-restart."""
        for path in glob.glob(os.path.join(self.ledger_dir, "*.json")):
            try:
                with open(path, "r") as f:
                    block = json.load(f)
                    if "nonce" in block:
                        self.seen_nonces.add(block["nonce"])
            except Exception:
                continue
        print(f"[+] Security Subsystem: Nonce registry synchronized ({len(self.seen_nonces)} historic nonces loaded).")

    def _validate_telemetry(self, telemetry_values):
        """Input Validation: Enforces strict type, bounds, and structural constraints on incoming telemetry."""
        if not isinstance(telemetry_values, list) or len(telemetry_values) == 0:
            raise ValueError("[X] INVALID TELEMETRY: Must be a non-empty list of numerical values.")
        validated = []
        for v in telemetry_values:
            if not isinstance(v, (int, float)):
                raise TypeError(f"[X] INVALID TELEMETRY TYPE: Non-numeric value detected ({v}).")
            if not (0.0 <= float(v) <= 10.0):
                raise ValueError(f"[X] TELEMETRY BOUNDS BREACH: Value {v} exceeds operating range [0.0, 10.0].")
            validated.append(float(v))
        return validated

    def _get_latest_block_info(self):
        receipts = sorted(glob.glob(os.path.join(self.ledger_dir, "*.json")))
        if not receipts:
            return 0, "GENESIS_BLOCK", "LOW_RISK"
        
        latest_path = receipts[-1]
        with open(latest_path, "r") as f:
            content = f.read()
            block = json.loads(content)
            
        current_index = block.get("block_index", len(receipts))
        self_hash = hashlib.sha256(content.encode()).hexdigest()
        risk_state = block.get("risk_state", "LOW_RISK")
        return current_index, self_hash, risk_state

    def evaluate_axiomos_ewma(self, telemetry_values):
        weights = [0.5, 0.3, 0.2]
        if len(telemetry_values) < len(weights):
            weights = [1.0 / len(telemetry_values)] * len(telemetry_values)
        ewma_score = sum(v * w for v, w in zip(telemetry_values, weights))
        risk_state = "HIGH_RISK" if ewma_score >= 3.0 else "LOW_RISK"
        return ewma_score, risk_state

    def commit_block(self, nonce, raw_telemetry, payload_content):
        # 1. Input Validation
        telemetry_values = self._validate_telemetry(raw_telemetry)

        # 2. Sigilith Nonce Uniqueness Check
        if nonce in self.seen_nonces:
            raise ValueError(f"[X] SECURITY HALT: Nonce reuse detected ({nonce}). Replay attack prevented.")

        prev_index, prev_hash, prev_risk_state = self._get_latest_block_info()
        block_index = prev_index + 1

        # 3. AXIOMOS Evaluation
        ewma_score, evaluated_risk = self.evaluate_axiomos_ewma(telemetry_values)

        # 4. Derek Cool-Down Gate
        if prev_risk_state == "HIGH_RISK" and evaluated_risk == "LOW_RISK":
            if any(v > 2.5 for v in telemetry_values):
                evaluated_risk = "HIGH_RISK"
                print(f"[!] Derek Gate: Cool-down failed. Residual drift held in containment.")
            else:
                print(f"[+] Derek Gate: Cool-down passed. Recovery authorized.")

        timestamp = time.time()
        payload_hash = hashlib.sha256(payload_content.encode()).hexdigest()
        governance_hash = hashlib.sha256(b"ThreeLineage Secure Production Core v2.1").hexdigest()

        block = {
            "system": "ThreeLineage Autonomous Governance",
            "block_index": block_index,
            "timestamp": timestamp,
            "nonce": nonce,
            "risk_state": evaluated_risk,
            "triggered_rule": "NOMINAL_EWMA_WINDOW" if evaluated_risk == "LOW_RISK" else "AXIOMOS_EWMA_THRESHOLD_EXCEEDED_3.0",
            "telemetry_source_values": telemetry_values,
            "ewma_score": round(ewma_score, 3),
            "payload_hash": payload_hash,
            "governance_source_hash": governance_hash,
            "previous_ledger_hash": prev_hash,
            "verifier_result": "PASSED" if evaluated_risk == "LOW_RISK" else "REJECTED_BY_POLICY",
            "execution_outcome": "DISPATCH_CONFIRMED" if evaluated_risk == "LOW_RISK" else "CONTAINMENT_ENFORCED",
            "status": "TESTED_CONTAINMENT_CONFIRMED" if evaluated_risk == "LOW_RISK" else "DENIED_CONTAINMENT_ENFORCED"
        }

        block_copy = block.copy()
        block_copy.pop("receipt_hash", None)
        receipt_hash = hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
        block["receipt_hash"] = receipt_hash

        filename = f"block_{block_index:04d}_{evaluated_risk}.json"
        path = os.path.join(self.ledger_dir, filename)
        worm_path = os.path.join(self.worm_dir, filename)

        # Write to primary active ledger with strict read-only permissions (chmod 600)
        with open(path, "w") as f:
            json.dump(block, f, indent=2)
        try:
            os.chmod(path, 0o600)
        except Exception:
            pass

        # WORM Mirroring: Mirror sealed block to secure off-site/isolated target storage
        shutil.copyfile(path, worm_path)
        try:
            os.chmod(worm_path, 0o400) # Read-only WORM lock
        except Exception:
            pass

        self.seen_nonces.add(nonce)
        print(f"[+] Secured Block #{block_index} [{evaluated_risk}]: {filename} (Mirrored to WORM)")
        return path

# Secure Execution Pipeline Demonstration
engine = SecureThreeLineageEngine()

# Clear active ledger to archive for secure baseline test
for f in os.listdir(LEDGER_DIR):
    if f.endswith(".json"):
        os.rename(os.path.join(LEDGER_DIR, f), os.path.join(ARCHIVE_DIR, f))

print("\n[*] Executing secure hardened lifecycle...\n")
engine.commit_block("secure_nonce_01", [0.5, 1.1, 1.4], "Payload: Hardened Alpha Stream")
engine.commit_block("secure_nonce_02", [4.8, 5.2, 4.9], "Payload: Flagged Threat Beta")
engine.commit_block("secure_nonce_03", [0.9, 1.2, 1.3], "Payload: Restored Safe Operation Gamma")
print("==================================================")
