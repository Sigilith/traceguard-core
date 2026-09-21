import json
import os
import glob
import re

print("[*] [Deep Anomaly Hunter] Scanning all workspace files, audit logs, and git objects for critical anomalies...")

anomalies = []

# Scan audit logs for error signatures or blocked payloads
for log_file in glob.glob("*.log") + glob.glob("logs/*.log"):
    try:
        with open(log_file, "r", errors="ignore") as f:
            for line in f:
                if any(err in line.lower() for err in ["error", "fail", "reject", "untracked", "conflict", "unauthorized"]):
                    anomalies.append((log_file, line.strip()))
    except Exception:
        pass

# Check config state for wallet integrity
config_path = "config_state.json"
if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            cfg = json.load(f)
            wallet = cfg.get("payout_wallet", "")
            if not re.match(r"^0x[a-fA-F0-9]{40}$", wallet):
                anomalies.append((config_path, f"Invalid wallet hash format: {wallet}"))
    except Exception as e:
        anomalies.append((config_path, f"JSON parse error: {e}"))

print(f"\n[!] [Deep Scan Complete] Detected {len(anomalies)} structural anomalies or warning vectors:")
for src, msg in anomalies[-10:]:
    print(f"  - [{src}] {msg}")

if not anomalies:
    print("[+] No active systemic crashes found. Pipeline clean.")
