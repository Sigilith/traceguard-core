import os
import json
import hashlib
import time
import glob

def banner(text):
    print("\n" + "=" * 50)
    print(f" {text}")
    print("=" * 50)

banner("THREE-LINEAGE LIVE DEMONSTRATION ENGINE")
time.sleep(1)

ledger_dir = ".lineage/derek_receipts"
archive_dir = ".lineage/archive"
os.makedirs(ledger_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

print("[*] Flushing legacy state and sanitizing environment...")
for f in os.listdir(ledger_dir):
    if f.endswith(".json"):
        os.rename(os.path.join(ledger_dir, f), os.path.join(archive_dir, f))
time.sleep(1)
print("[+] Environment clean. Initializing Genesis state.\n")
time.sleep(1)

def create_block(timestamp, nonce, risk_state, payload, prev_hash):
    block = {
        "system": "ThreeLineage Autonomous Governance",
        "timestamp": timestamp,
        "nonce": nonce,
        "risk_state": risk_state,
        "triggered_rule": "NOMINAL_WINDOW" if risk_state == "LOW_RISK" else "AXIOMOS_THRESHOLD_EXCEEDED_3.0",
        "telemetry_source_values": [0.5, 1.2, 1.8] if risk_state == "LOW_RISK" else [4.2, 5.1, 4.8],
        "rolling_average": 1.17 if risk_state == "LOW_RISK" else 4.7,
        "payload_hash": hashlib.sha256(payload.encode()).hexdigest(),
        "governance_source_hash": hashlib.sha256(b"ThreeLineage Core v1.0").hexdigest(),
        "previous_ledger_hash": prev_hash,
        "verifier_result": "PASSED" if risk_state == "LOW_RISK" else "REJECTED_BY_POLICY",
        "execution_outcome": "DISPATCH_CONFIRMED" if risk_state == "LOW_RISK" else "CONTAINMENT_ENFORCED",
        "status": "TESTED_CONTAINMENT_CONFIRMED" if risk_state == "LOW_RISK" else "DENIED_CONTAINMENT_ENFORCED"
    }
    
    block_copy = block.copy()
    block_copy.pop("receipt_hash", None)
    receipt_hash = hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
    block["receipt_hash"] = receipt_hash
    
    filename = f"block_{int(timestamp)}_{risk_state}.json"
    path = os.path.join(ledger_dir, filename)
    with open(path, "w") as f:
        json.dump(block, f, indent=2)
        
    with open(path, "r") as f:
        content = f.read()
    return hashlib.sha256(content.encode()).hexdigest(), filename, receipt_hash

banner("STAGE 1: RECORDING GOVERNANCE TRANSITIONS")
t1 = 1788728900.0
h1, f1, r1 = create_block(t1, "b7dfe39617fdab46", "LOW_RISK", "Outreach Target: Success Flow", "GENESIS_BLOCK")
print(f"[+] Block 1 Sealed [LOW_RISK]: {f1}")
print(f"    -> Self Hash: {r1[:16]}...")
time.sleep(1.2)

t2 = 1788728905.0
h2, f2, r2 = create_block(t2, "4260dcf375fd53a4", "HIGH_RISK", "Outreach Target: Quarantined Flow", h1)
print(f"[+] Block 2 Sealed [HIGH_RISK]: {f2}")
print(f"    -> Linked Prev: {h1[:16]}...")
print(f"    -> Self Hash: {r2[:16]}...")
time.sleep(1.2)

t3 = 1788728910.0
h3, f3, r3 = create_block(t3, "9c81a2bb33fbc111", "LOW_RISK", "Outreach Target: Resumed Flow", h2)
print(f"[+] Block 3 Sealed [LOW_RISK]: {f3}")
print(f"    -> Linked Prev: {h2[:16]}...")
print(f"    -> Self Hash: {r3[:16]}...")
time.sleep(1.5)

banner("STAGE 2: EXECUTING TRACEGUARD INTEGRITY VERIFICATION")
time.sleep(1)

receipts = sorted(glob.glob(os.path.join(ledger_dir, "*.json")))
expected_prev = "GENESIS_BLOCK"
chain_valid = True

for path in receipts:
    with open(path, "r") as f:
        content = f.read()
    block = json.loads(content)
    file_name = os.path.basename(path)
    
    if block.get("previous_ledger_hash") != expected_prev:
        print(f"[X] BROKEN LINK at {file_name}")
        chain_valid = False
    
    block_copy = block.copy()
    block_copy.pop("receipt_hash", None)
    recalculated = hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
    
    if block.get("receipt_hash") != recalculated:
        print(f"[X] HASH MISMATCH at {file_name}")
        chain_valid = False
    else:
        print(f"[+] Verified Block: {file_name} [INTEGRITY SECURE]")
    
    time.sleep(0.8)
    expected_prev = hashlib.sha256(content.encode()).hexdigest()

banner("FINAL VERDICT")
time.sleep(0.5)
if chain_valid:
    print(" LEDGER STATUS: 100% CRYPTOGRAPHICALLY INTACT.")
else:
    print(" LEDGER STATUS: TAMPERING DETECTED.")
print("=" * 50 + "\n")
