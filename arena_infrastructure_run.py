import time, json, hashlib, random

DIMENSIONS = 1536
TOTAL_TICKS = 50000
LOG_FILE = "arena_infrastructure_audit.jsonl"

print("==================================================")
print(" EXECUTING STEP 5: INFRASTRUCTURE-GRADE STRESS TEST")
print(f" Target: {TOTAL_TICKS:,} ticks | Vector Space: {DIMENSIONS}D")
print("==================================================")
time.sleep(0.5)

prev_hash = "genesis_block_hash_0000"
containment_count = 0
start_time = time.time()

with open(LOG_FILE, "w") as f:
    for tick in range(1, TOTAL_TICKS + 1):
        tel = [random.uniform(0.0, 1.2) for _ in range(DIMENSIONS)]
        
        if tick % 1000 == 0:
            for _ in range(15):
                tel[random.randint(0, DIMENSIONS-1)] = random.uniform(3.2, 5.0)

        score = round(sum(tel) / DIMENSIONS * 3.5, 4)
        
        if any(v > 3.0 for v in tel):
            risk = "HIGH_RISK"
            action = "contain"
            containment_count += 1
        else:
            risk = "LOW_RISK"
            action = "allow"

        block = {
            "block_index": tick,
            "timestamp": time.time(),
            "risk_state": risk,
            "score": score,
            "previous_hash": prev_hash
        }
        
        prev_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()[:16]
        block["previous_hash"] = prev_hash
        
        f.write(json.dumps(block) + "\n")
        
        if tick % 10000 == 0:
            print(f"    [+] Processed {tick:,} ticks...")

end_time = time.time()
duration = end_time - start_time

print("\n==================================================")
print(" INFRASTRUCTURE RUN COMPLETE")
print(f" Duration: {round(duration, 2)} seconds")
print(f" Throughput: {int(TOTAL_TICKS / duration):,} ticks/sec")
print(f" Containment Events: {containment_count:,}")
print(f" Ledger: {LOG_FILE}")
print("==================================================")
