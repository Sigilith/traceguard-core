import json
with open(".lineage/collisions.jsonl") as f:
    for line in f:
        if not line.strip(): continue
        ev = json.loads(line)
        print(f"Event: {ev['event_id'][:8]}... | Step: {ev['step']:<25} | Type: {ev['failure_type']:<20}")
        print(f"  -> Prev Hash: {ev['previous_evidence_hash'][:16]}...")
        print(f"  -> Curr Hash: {ev['evidence_hash'][:16]}...\n")
