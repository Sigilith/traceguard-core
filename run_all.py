import time, json, hashlib, random
import traceguard.core as traceguard
import sigilith.analysis as sigilith

LOG_FILE = "three_lineage_audit.jsonl"
prev_hash = "genesis_block_hash_0000"

with open(LOG_FILE, "w") as f:
    for i in range(1, 16):
        tel = [3.4, 4.1, 2.8] if i in [4, 8, 12] else [round(random.uniform(0.2, 0.9), 2), round(random.uniform(0.3, 0.8), 2), round(random.uniform(0.2, 0.7), 2)]
        nonce = traceguard.generate_bound_nonce(prev_hash)
        risk = "HIGH_RISK" if any(v > 2.5 for v in tel) else "LOW_RISK"
        block = {
            "block_index": i,
            "timestamp": time.time(),
            "nonce": nonce,
            "risk_state": risk,
            "telemetry": tel,
            "score": round(sum(tel)/len(tel), 3),
            "previous_hash": prev_hash
        }
        prev_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()[:16]
        f.write(json.dumps(block) + "\n")

print("==================================================")
print(" THREE-LINEAGE AUDIT: LINKEDIN SNIPPET (BLOCKS 4 & 5)")
print("==================================================")
lines = open(LOG_FILE).readlines()
print(json.dumps(json.loads(lines[3]), indent=2))
print(json.dumps(json.loads(lines[4]), indent=2))
print("==================================================")
