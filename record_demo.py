import time, json, hashlib, random
import traceguard.core as traceguard

print("==================================================")
print(" THREE-LINEAGE LIVE RUNTIME MONITOR")
print("==================================================")
time.sleep(1)

prev_hash = "genesis_block_hash_0000"

for i in range(1, 6):
    tel = [3.4, 4.1, 2.8] if i == 4 else [round(random.uniform(0.3, 0.8), 2), round(random.uniform(0.4, 0.7), 2), round(random.uniform(0.2, 0.6), 2)]
    nonce = traceguard.generate_bound_nonce(prev_hash)
    risk = "HIGH_RISK" if i == 4 else "LOW_RISK"
    
    if i == 4:
        print(f"\n[!] [Block #{i}] Derek Gate: High-Risk spike detected {tel}")
        time.sleep(1.2)
        print(f"[!] [Derek Gate] Triple-Lock Failed: Containment Enforced.")
        time.sleep(1.0)
    
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
    
    print(f"[+] Sealed Block #{i} | Risk: {risk:<10} | Hash: {prev_hash}")
    time.sleep(0.8)

print("\n==================================================")
print(" DEMO COMPLETE: SYSTEM SECURE")
print("==================================================")
