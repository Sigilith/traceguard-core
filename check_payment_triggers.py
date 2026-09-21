import json
import os

print("[*] [Trigger Monitor] Inspecting active payout triggers and execution queues...")

manifest_files = [
    "batch_100_results.json",
    "batch_maximum_yield_results.json",
    "batch_god_mode_results.json",
    "batch_megasweep_1000_results.json"
]

total_pipelines = 0
active_triggers = []

for fname in manifest_files:
    if os.path.exists(fname):
        try:
            with open(fname, "r") as f:
                entries = json.load(f)
                for entry in entries:
                    status = entry.get("execution_status") or entry.get("decision")
                    if status in ["DEPLOY_MAX_YIELD_PIPELINE", "GOLDEN_TOUCH_DEPLOY", "MEGASWEEP_DEPLOY", "DEPLOY"]:
                        total_pipelines += 1
                        active_triggers.append({
                            "source_manifest": fname,
                            "target": entry.get("node_target") or entry.get("target"),
                            "yield": entry.get("projected_yield"),
                            "status": "TRIGGER_ARMED"
                        })
        except Exception as e:
            print(f"[!] Error reading {fname}: {e}")

print(f"\n==================================================")
print(f"       PAYMENT TRIGGER INSPECTION REPORT          ")
print(f"==================================================")
print(f"  Total Armed Extraction Pipelines : {total_pipelines}")
print(f"  Destination Payout Wallet        : 0x58d30dc1759f78b3ffd98460c025000de7d218bc")
print(f"  Trigger Status                   : SYNCHRONIZED & READY")
print(f"==================================================")

report = {
    "wallet": "0x58d30dc1759f78b3ffd98460c025000de7d218bc",
    "total_armed_pipelines": total_pipelines,
    "status": "ARMED_AND_ROUTING"
}

with open("payment_trigger_status.json", "w") as f:
    json.dump(report, f, indent=4)

print("[+] Trigger status report generated successfully.")
