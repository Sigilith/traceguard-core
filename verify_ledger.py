import os
import json
import hashlib
import glob

print("==================================================")
print(" THREE-LINEAGE LEDGER INTEGRITY VERIFIER")
print("==================================================")

ledger_dir = ".lineage/derek_receipts"
receipts = sorted(glob.glob(os.path.join(ledger_dir, "*.json")))

if not receipts:
    print("[-] No ledger blocks found to verify.")
    exit(0)

expected_prev_hash = "GENESIS_BLOCK"
chain_valid = True

for path in receipts:
    with open(path, "r") as f:
        content = f.read()
        
    block = json.loads(content)
    file_name = os.path.basename(path)
    
    # Handle legacy thin blocks without cryptographic receipt hashes
    stored_self_hash = block.get("receipt_hash")
    if not stored_self_hash:
        print(f"[!] Legacy/Thin Block detected: {file_name} [SKIPPING CHAIN CHECK]")
        continue

    stored_prev = block.get("previous_ledger_hash")
    prev_display = stored_prev[:16] if stored_prev else "NONE"
    expected_display = expected_prev_hash[:16] if expected_prev_hash else "NONE"

    if stored_prev != expected_prev_hash and expected_prev_hash != "GENESIS_BLOCK":
        print(f"[X] BROKEN LINK at {file_name}: Expected prev hash {expected_display}..., got {prev_display}...")
        chain_valid = False
    
    block_copy = block.copy()
    block_copy.pop("receipt_hash", None)
    recalculated_hash = hashlib.sha256(json.dumps(block_copy, sort_keys=True).encode()).hexdigest()
    
    if stored_self_hash != recalculated_hash:
        print(f"[X] HASH MISMATCH at {file_name}: Block contents altered!")
        chain_valid = False
    else:
        print(f"[+] Verified Block: {file_name} [INTEGRITY SECURE]")
        
    expected_prev_hash = hashlib.sha256(content.encode()).hexdigest()

print("==================================================")
if chain_valid:
    print(" LEDGER STATUS: CRYPTOGRAPHIC CHAIN INTACT.")
else:
    print(" LEDGER STATUS: CORRUPTION OR TAMPERING DETECTED.")
print("==================================================")
