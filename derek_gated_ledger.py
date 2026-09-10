import os
import json
import time
import hashlib
import glob

print("==================================================")
print(" THREE-LINEAGE ENHANCED LEDGER & DEREK GATE ENGINE")
print("==================================================")

ledger_dir = ".lineage/derek_receipts"
os.makedirs(ledger_dir, exist_ok=True)

def get_previous_ledger_hash():
    """Finds the most recent receipt and calculates its SHA-256 for chaining."""
    receipts = sorted(glob.glob(os.path.join(ledger_dir, "*.json")))
    if not receipts:
        return "GENESIS_BLOCK"
    latest_receipt_path = receipts[-1]
    with open(latest_receipt_path, "r") as f:
        content = f.read()
    return hashlib.sha256(content.encode()).hexdigest()

def seal_receipt(nonce, drifts, risk_state, payload_content, status):
    prev_hash = get_previous_ledger_hash()
    timestamp = time.time()
    
    # Compute payload hash
    payload_hash = hashlib.sha256(payload_content.encode()).hexdigest()
    
    # Base receipt structure before self-hashing
    receipt = {
        "system": "ThreeLineage Autonomous Governance",
        "timestamp": timestamp,
        "nonce": nonce,
        "risk_state": risk_state,
        "triggered_rule": "AXIOMOS_THRESHOLD_EXCEEDED_3.0" if risk_state == "HIGH_RISK" else "NOMINAL_WINDOW",
        "telemetry_source_values": drifts,
        "rolling_average": sum(drifts) / len(drifts),
        "payload_hash": payload_hash,
        "governance_source_hash": hashlib.sha256(b"ThreeLineage Core v1.0").hexdigest(),
        "previous_ledger_hash": prev_hash,
        "verifier_result": "PASSED" if risk_state == "LOW_RISK" else "REJECTED_BY_POLICY",
        "execution_outcome": "DISPATCH_CONFIRMED" if risk_state == "LOW_RISK" else "CONTAINMENT_ENFORCED",
        "status": status
    }
    
    # Generate receipt hash
    receipt_string = json.dumps(receipt, sort_keys=True)
    receipt_hash = hashlib.sha256(receipt_string.encode()).hexdigest()
    receipt["receipt_hash"] = receipt_hash
    
    # Write block to disk
    receipt_filename = f"block_{int(timestamp)}_{risk_state}.json"
    receipt_path = os.path.join(ledger_dir, receipt_filename)
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)
        
    print(f"[+] Cryptographic block sealed: {receipt_path}")
    print(f"    -> Link Hash (Prev): {prev_hash[:16]}...")
    print(f"    -> Block Hash (Self): {receipt_hash[:16]}...")

# Example test run: Simulating a High-Risk Anomaly Block
nonce = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
drifts = [4.2, 5.1, 4.8]
risk_state = "HIGH_RISK"
payload = "Outreach Payload Target: enterprise-uk-target.co.uk"

seal_receipt(nonce, drifts, risk_state, payload, "DENIED_CONTAINMENT_ENFORCED")
print("==================================================")
