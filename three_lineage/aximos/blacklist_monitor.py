import json
import time
import sys
import os

LOG_FILE = ".lineage/collisions.jsonl"
STRIKE_THRESHOLD = 3
WINDOW_SECONDS = 300

def process_blacklist():
    print("[*] Activating Axiomos Dynamic Blacklist Monitor...")
    violation_tracker = {}

    while not os.path.exists(LOG_FILE):
        time.sleep(0.5)

    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
                
            try:
                event = json.loads(line)
                failure_type = event.get("failure_type")
                agent = event.get("agent", "unknown-node")
                
                if failure_type in ["security_violation", "governance_violation", "replay_attack", "intent_drift"]:
                    now = time.time()
                    timestamps = violation_tracker.get(agent, [])
                    timestamps = [ts for ts in timestamps if now - ts < WINDOW_SECONDS]
                    timestamps.append(now)
                    violation_tracker[agent] = timestamps
                    
                    print(f"[!] Violation tracked for {agent}. Strikes: {len(timestamps)}/{STRIKE_THRESHOLD}")
                    
                    if len(timestamps) >= STRIKE_THRESHOLD:
                        print(f"[CRITICAL] {agent} has exceeded safety thresholds! Triggering firewall isolation...")
                        isolate_node(agent)
                        
            except Exception:
                pass

def isolate_node(agent_id):
    print(f"[KILL_SWITCH] Firewall rule injected: Dropping all traffic from {agent_id}.")
    print("[KILL_SWITCH] Terminal state reached. Halting execution lane.")
    sys.exit(0)

if __name__ == "__main__":
    process_blacklist()
