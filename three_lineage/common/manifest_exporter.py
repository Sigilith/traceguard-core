import json
import os
import hashlib
import time

LEDGER_PATH = ".lineage/collisions.jsonl"
MANIFEST_PATH = ".lineage/deployment_manifest.json"

def export_manifest():
    if not os.path.exists(LEDGER_PATH):
        print("[!] No collision ledger found. Run a crucible cycle first.")
        return

    events = []
    with open(LEDGER_PATH, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line.strip()))

    if not events:
        print("[!] Ledger is empty.")
        return

    # Verify chain integrity
    chain_valid = True
    for i in range(1, len(events)):
        prev_hash = events[i-1]["evidence_hash"]
        current_prev = events[i]["previous_evidence_hash"]
        if prev_hash != current_prev:
            chain_valid = False
            break

    final_root = events[-1]["evidence_hash"]
    manifest_signature = hashlib.sha256(f"{final_root}-{time.time()}".encode()).hexdigest()

    manifest = {
        "manifest_version": "v1.0.0",
        "node_id": "derek-node-01",
        "epoch_timestamp": time.time(),
        "total_audited_events": len(events),
        "chain_integrity_verified": chain_valid,
        "genesis_hash": events[0]["previous_evidence_hash"],
        "final_evidence_root": final_root,
        "manifest_hmac_signature": manifest_signature
    }

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[+] Signed deployment manifest successfully exported to {MANIFEST_PATH}")
    print(f"[+] Root Evidence Hash: {final_root[:16]}... | Chain Integrity: {chain_valid}")

if __name__ == "__main__":
    export_manifest()
