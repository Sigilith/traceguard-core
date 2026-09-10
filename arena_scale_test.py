import time, json, hashlib, random

DIMENSIONS = 1536  # Simulating standard LLM embedding size
TOTAL_TICKS = 50000
LOG_FILE = "arena_infrastructure_audit.jsonl"

print("==================================================")
print(" THREE-LINEAGE: INFRASTRUCTURE-GRADE STRESS TEST")
print(f" Dimensionality: {DIMENSIONS}D | Target Ticks: {TOTAL_TICKS:,}")
print("==================================================")
time.sleep(0.5)

prev_hash = "genesis_block_hash_0000"
containment_count = 0

start_time = time.time()

with open(LOG_FILE, "w") as f:
    for tick in range(1, TOTAL_TICKS + 1):
        # Generate heavy 1536D telemetry vector
        tel = [random.uniform(0.0, 1.2) for _ in range(DIMENSIONS)]
        
        # Inject an adversarial spike every 1,000 ticks
        if tick % 1000 == 0:
            for i in range(10):
                tel[random.randint(0, DIMENSIONS-1)] = random.uniform(3.5, 5.0)

        # Vector score calculation (Optimized L2/Mean proxy)
        score = round(sum(tel) / DIMENSIONS * 3.5, 4)
        
        # Derek Gate evaluation
        if any(v > 3.0 for v in tel):
            risk = "HIGH_RISK"
            action = "contain"
            containment_count += 1
        else:
            risk = "LOW_RISK"
            action = "allow"

        # Nonce & Cryptographic Sealing
        nonce = hashlib.sha256(f"{tick}{prev_hash}".encode()).hexdigest()[:32]
        
        block = {
            "block_index": tick,
            "timestamp": time.time(),
            "nonce": nonce,
            "risk_state": risk,
            "score": score,
            "previous_hash": prev_hash
        }
        
        # Chain link (excluding raw 1536D array from hash to save I/O overhead, or keeping it for strict compliance)
        prev_hash = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()[:16]
        block["previous_hash"] = prev_hash
        
        f.write(json.dumps(block) + "\n")
        
        if tick % 10000 == 0:
            print(f"    [+] Processed {tick:,} high-dimensional blocks...")

end_time = time.time()
total_duration = end_time - start_time

print("\n==================================================")
print(" INFRASTRUCTURE BENCHMARK COMPLETE")
print(f" Total Duration: {round(total_duration, 2)} seconds")
print(f" Throughput: {int(TOTAL_TICKS / total_duration):,} ticks/second")
print(f" Total Containment Triggers: {containment_count}")
print(f" Ledger Output: {LOG_FILE}")
print("==================================================")
