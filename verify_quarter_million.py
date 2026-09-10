import json, hashlib, time

LOG_FILE = "arena_quarter_million_audit.jsonl"

print("==================================================")
print(" THREE-LINEAGE: QUARTER-MILLION LEDGER VERIFICATION")
print(f" Target: {LOG_FILE}")
print("==================================================")
time.sleep(0.5)

start_time = time.time()
expected_hash = "genesis_block_hash_0000"
valid_blocks = 0
fracture_found = False

try:
    with open(LOG_FILE, "r") as f:
        for line in f:
            block = json.loads(line)
            
            if block["previous_hash"] != expected_hash:
                print(f"\n[!] FATAL: Chain fracture detected at Block {block['block_index']}")
                print(f"    Expected: {expected_hash}")
                print(f"    Found:    {block['previous_hash']}")
                fracture_found = True
                break
            
            expected_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()[:16]
            valid_blocks += 1
            
            if valid_blocks % 50000 == 0:
                print(f"    [+] Verified {valid_blocks:,} blocks...")

except FileNotFoundError:
    print(f"[!] Error: {LOG_FILE} not found.")
    exit(1)

end_time = time.time()

if not fracture_found:
    print("\n==================================================")
    print(" VERIFICATION COMPLETE: ZERO FRACTURES")
    print(f" Cryptographic Lineage Validated: {valid_blocks:,}/250,000 Blocks")
    print(f" Sweep Time: {round(end_time - start_time, 2)} seconds")
    print("==================================================")
