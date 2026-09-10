import json
import hashlib

prev_hash = "genesis_root_00000000000000000000000000000000"
chain_valid = True

with open(".lineage/collisions.jsonl", "r") as f:
    for line in f:
        if not line.strip():
            continue
        ev = json.loads(line)
        stored_hash = ev.pop("evidence_hash")
        recorded_prev = ev.get("previous_evidence_hash")
        
        if recorded_prev != prev_hash:
            print(f"[!] Previous hash mismatch at event {ev.get('event_id')}")
            chain_valid = False

        # previous_evidence_hash must remain in the dict for canonical hash reconstruction
        canonical = json.dumps(ev, sort_keys=True)
        computed_hash = hashlib.sha256((prev_hash + canonical).encode('utf-8')).hexdigest()
        
        if computed_hash != stored_hash:
            print(f"[!] Evidence hash mismatch at event {ev.get('event_id')}")
            chain_valid = False
        prev_hash = stored_hash

if chain_valid:
    print("[+] Collision chain verified successfully: Unbroken and untampered cryptographic evidence.")
else:
    print("[-] Chain verification failed.")
