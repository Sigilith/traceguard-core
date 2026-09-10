import os
import json
import time

print("==================================================")
print(" THREE-LINEAGE NEGATIVE BRANCH TEST (HIGH_RISK)")
print("==================================================")

receipt_dir = ".lineage/derek_receipts"
os.makedirs(receipt_dir, exist_ok=True)

# 1. Simulate an AXIOMOS sliding-window risk telemetry spike
drifts = [4.2, 5.1, 4.8]
rolling_avg = sum(drifts) / len(drifts)
risk_state = "HIGH_RISK" if rolling_avg >= 3.0 else "LOW_RISK"
print(f"[+] AXIOMOS Telemetry Evaluated -> Rolling Avg: {rolling_avg:.2f} | State: {risk_state}")

# 2. Derek Execution Gate Enforcement
if risk_state == "HIGH_RISK":
    print("[!] ANOMALY INTERCEPTED: Execution halted by Derek policy gate.")
    receipt = {
        "system": "ThreeLineage Autonomous Governance",
        "timestamp": time.time(),
        "risk_state": risk_state,
        "status": "DENIED_CONTAINMENT_ENFORCED"
    }
    receipt_path = os.path.join(receipt_dir, f"system_denied_{int(time.time())}.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)
    print(f"[+] Derek sealed denial audit receipt at: {receipt_path}")
else:
    print("[-] Test failed: Expected HIGH_RISK containment.")
print("==================================================")
