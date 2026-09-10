import json
import time
import os
import fcntl

LINEAGE_FILE = ".lineage/collisions.jsonl"
STATE_FILE = ".lineage/contract_state.json"

ENTROPY_THRESHOLD = 4.2
AST_DEPTH_THRESHOLD = 4
VELOCITY_THRESHOLD_SEC = 0.05
DRIFT_TOLERANCE_LIMIT = 5.0

def enforce_quarantine():
    if not os.path.exists(STATE_FILE):
        return
    
    print(f"\n[!] ENGAGING ACTIVE QUARANTINE PROTOCOL...")
    try:
        with open(STATE_FILE, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            state_data = json.load(f)
            
            quarantined_count = 0
            for cid, contract in state_data.items():
                if not contract.get("consumed", False):
                    contract["current_state"] = "S_QUARANTINE_LOCKED"
                    contract["consumed"] = True
                    quarantined_count += 1
            
            f.seek(0)
            json.dump(state_data, f, indent=2)
            f.truncate()
            fcntl.flock(f, fcntl.LOCK_UN)
            
        print(f"[SUCCESS] {quarantined_count} active contracts forcefully consumed and quarantined.")
    except Exception as e:
        print(f"[CRITICAL] Quarantine enforcement failed: {e}")

def analyze_behavioural_regime():
    if not os.path.exists(LINEAGE_FILE):
        return

    with open(LINEAGE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return

    total_drift_score = 0.0
    last_timestamp = None

    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
            
        metrics = record.get("metrics", {})
        entropy = metrics.get("entropy", 0.0)
        ast_depth = metrics.get("ast_depth", 0)
        ts = record.get("timestamp", 0.0)

        velocity_delta = (ts - last_timestamp) if last_timestamp and ts else 1.0
        if ts: last_timestamp = ts

        entropy_drift = max(0.0, entropy - ENTROPY_THRESHOLD)
        ast_drift = max(0, ast_depth - AST_DEPTH_THRESHOLD)
        velocity_drift = 1.0 if velocity_delta < VELOCITY_THRESHOLD_SEC else 0.0

        total_drift_score += (entropy_drift * 2.0) + (ast_drift * 1.5) + (velocity_drift * 3.0)

    print(f"====================================================")
    print(f"[SUMMARY] Aggregate Agent Behavioural Drift Score: {total_drift_score:.2f}")
    
    if total_drift_score > DRIFT_TOLERANCE_LIMIT:
        print(f"[ALERT] REGIME DRIFT DETECTED: Agent behavior exceeds safety tolerance!")
        enforce_quarantine()
    else:
        print(f"[STATUS] REGIME STABLE: Agent operates within nominal bounds.")
    print(f"====================================================\n")

if __name__ == "__main__":
    analyze_behavioural_regime()
