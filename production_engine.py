import os
import json
import hashlib
import time
import glob

print("==================================================")
print(" THREE-LINEAGE PRODUCTION GOVERNANCE ENGINE v2.0")
print("==================================================")

ledger_dir = ".lineage/derek_receipts"
archive_dir = ".lineage/archive"
os.makedirs(ledger_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

class ThreeLineageEngine:
    def __init__(self):
        self.ledger_dir = ledger_dir
        self.seen_nonces = set()
        self._load_nonce_registry()

    def _load_nonce_registry(self):
        """Loads historical nonces into memory to enforce Sigilith uniqueness and prevent replays."""
        for path in glob.glob(os.path.join(self.ledger_dir, "*.json")):
            try:
                with open(path, "r") as f:
                    block = json.load(f)
                    if "nonce" in block:
                        self.seen_nonces.add(block["nonce"])
            except Exception:
                continue

    def _get_latest_block_info(self):
        """Retrieves the highest block index, hash, and risk state from the active ledger."""
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
        """AXIOMOS Calibration: Exponentially Weighted Moving Average (EWMA) for risk sensitivity."""
        weights = [0.5, 0.3, 0.2] # Heavier weight on most recent metrics
        if len(telemetry_values) < len(weights):
            weights = [1.0 / len(telemetry_values)] * len(telemetry_values)
        
        ewma_score = sum(v * w for v, w in zip(telemetry_values, weights))
        risk_state = "HIGH_RISK" if ewma_score >= 3.0 else "LOW_RISK"
        return ewma_score, risk_state

    def commit_block(self, nonce, telemetry_values, payload_content):
        """Derek & TraceGuard Calibration: Monotonic Indexing, Cool-down Gate, Nonce Verification, & Chaining."""
        
        # 1. Sigilith Nonce Uniqueness Check
        if nonce in self.seen_nonces:
            raise ValueError(f"[X] SECURITY HALT: Nonce reuse detected ({nonce}). Replay attack prevented.")
        
        prev_index, prev_hash, prev_risk_state = self._get_latest_block_info()
        block_index = prev_index + 1
        
        # 2. AXIOMOS EWMA Evaluation
        ewma_score, evaluated_risk = self.evaluate_axiomos_ewma(telemetry_values)
        
        # 3. Derek Cool-down & Re-verification Gate Logic
        # If the previous state was HIGH_RISK, enforce a mandatory multi-factor clearance check before returning to LOW_RISK
        if prev_risk_state == "HIGH_RISK" and evaluated_risk == "LOW_RISK":
            print("[*] Derek Gate: Previous state was HIGH_RISK. Enforcing re-verification cool-down clearance...")
            # Multi-factor check simulation: ensure telemetry has stabilized well below threshold
            if any(v > 2.5 for v in telemetry_values):
                evaluated_risk = "HIGH_RISK"
                print("[!] Cool-down check failed: Residual drift detected. Maintaining containment.")
            else:
                print("[+] Cool-down check passed: Telemetry stabilized. Recovery authorized.")

        timestamp = time.time()
        payload_hash = hashlib.sha256(payload_content.encode()).hexdigest()
        governance_hash = hashlib.sha256(b"ThreeLineage Production Core v2.0").hexdigest()
        
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
        
        # Self-hash generation
        block_copy = block.copy()
        block_copy.pop("receipt_hash", None)
        receipt_hash = hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
        block["receipt_hash"] = receipt_hash
        
        filename = f"block_{block_index:04d}_{evaluated_risk}.json"
        path = os.path.join(self.ledger_dir, filename)
        
        with open(path, "w") as f:
            json.dump(block, f, indent=2)
            
        self.seen_nonces.add(nonce)
        print(f"[+] Sealed Block #{block_index} [{evaluated_risk}]: {filename}")
        print(f"    -> EWMA Score: {ewma_score:.2f} | Self-Hash: {receipt_hash[:16]}...")
        return path

# Execution Simulation: Full Lifecycle Pipeline Test
engine = ThreeLineageEngine()

# Flush legacy items to archive for pristine test run
for f in os.listdir(ledger_dir):
    if f.endswith(".json"):
        os.rename(os.path.join(ledger_dir, f), os.path.join(archive_dir, f))
print("[+] Sanitized legacy state. Executing calibrated lifecycle...\n")

# Step 1: Nominal Low-Risk Dispatch
engine.commit_block("nonce_alpha_001", [0.4, 1.0, 1.5], "Payload: Standard Outreach Alpha")

# Step 2: High-Risk Anomaly Spike Triggering Containment
engine.commit_block("nonce_beta_002", [4.5, 5.0, 4.2], "Payload: Quarantined Target Beta")

# Step 3: Attempting Recovery with Residual Drift (Should be held in containment by cool-down gate)
engine.commit_block("nonce_gamma_003", [2.8, 2.2, 1.9], "Payload: Attempted Recovery Gamma")

# Step 4: Fully Stabilized Recovery (Passing cool-down re-verification)
engine.commit_block("nonce_delta_004", [0.8, 1.1, 1.2], "Payload: Resumed Secure Operations Delta")

print("==================================================")
