import json
import os
from alert_dispatcher import send_alert

BASELINE_FILE = "baseline.json"
CURRENT_FILE = "live_targets.txt"

def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_baseline(targets):
    with open(BASELINE_FILE, "w") as f:
        json.dump(list(targets), f, indent=2)

def detect_changes():
    baseline = load_baseline()
    
    if not os.path.exists(CURRENT_FILE):
        print(f"[-] File {CURRENT_FILE} not found.")
        return []

    with open(CURRENT_FILE, "r") as f:
        current_targets = set(line.strip() for line in f if line.strip())
        
    new_assets = current_targets - baseline
    removed_assets = baseline - current_targets
    
    if new_assets:
        print(f"[+] Detected {len(new_assets)} new asset(s):")
        for asset in new_assets:
            print(f"  - {asset}")
        # Send the actual discovered targets to the webhook
        send_alert(list(new_assets))
            
    if removed_assets:
        print(f"[-] Removed {len(removed_assets)} asset(s):")
        for asset in removed_assets:
            print(f"  - {asset}")
            
    save_baseline(current_targets)
    return list(new_assets)

if __name__ == "__main__":
    detect_changes()
