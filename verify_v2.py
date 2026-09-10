import os
import json
import hashlib
import glob

print("==================================================")
print(" THREE-LINEAGE v2.0 INTEGRITY & REPLAY VERIFIER")
print("==================================================")

ledger_dir = ".lineage/derek_receipts"
receipts = sorted(glob.glob(os.path.join(ledger_dir, "*.json")))

if not receipts:
    print("[-] No ledger blocks found to verify.")
    exit(0)

expected_prev_hash = "GENESIS_BLOCK"
expected_index = 1
seen_nonces = set()
chain_valid = True

for path in receipts:
    with open(path, "r") as f:
        content = f.read()
        
    block = json.loads(content)
    file_name = os.path.basename(path)
    
    # 1. Verify Monotonic Block Index
    b_index = block.get("block_index")
    if b_index != expected_index:
        print(f"[X] INDEX ANOMALY at {file_name}: Expected index {expected_index}, got {b_index}")
        chain_valid = False

    # 2. Verify Nonce Uniqueness (Replay Attack Detection)
    nonce = block.get("nonce")
    if nonce in seen_nonces:
        print(f"[X] REPLAY DETECTED at {file_name}: Duplicate nonce '{nonce}' found!")
        chain_valid = False
    seen_nonces.add(nonce)

    # 3. Verify Previous Hash Linkage
    stored_prev = block.get("previous_ledger_hash")
    if stored_prev != expected_prev_hash and expected_index > 1:
        prev_display = stored_prev[:16] if stored_prev else "NONE"
        expected_display = expected_prev_hash[:16] if expected_prev_hash else "NONE"
        print(f"[X] BROKEN LINK at {file_name}: Expected prev hash {expected_display}..., got {prev_display}...")
        chain_valid = False
    
    # 4. Verify Self-Hash Integrity
    stored_self_hash = block.get("receipt_hash")
    block_copy = block.copy()
    block_copy.pop("receipt_hash", None)
    recalculated_hash = hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
    
    if stored_self_hash != recalculated_hash:
        print(f"[X] HASH MISMATCH at {file_name}: Block contents altered!")
        chain_valid = False
    else:
        print(f"[+] Verified Block #{b_index} ({file_name}) [INTEGRITY SECURE]")
        
    expected_prev_hash = hashlib.sha256(content.encode()).hexdigest()
    expected_index += 1

print("==================================================")
if chain_valid:
    print(" LEDGER STATUS: 100% CRYPTOGRAPHICALLY INTACT & REPLAY-SECURE.")
else:
    print(" LEDGER STATUS: CORRUPTION, BREAKAGE, OR REPLAY DETECTED.")
print("==================================================")
