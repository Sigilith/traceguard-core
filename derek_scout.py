import time
import json
import uuid
from pathlib import Path

INBOUND_DIR = Path(".lineage/inbound_work")
PROCESSED_DIR = Path(".lineage/processed_work")
RECEIPTS_DIR = Path(".lineage/derek_receipts")
PAYPAL_HANDLE = "Kynash1"

def initialize_directories():
    for d in [INBOUND_DIR, PROCESSED_DIR, RECEIPTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def run_scout_loop():
    initialize_directories()
    print(f"[*] Derek Scout active. Monitoring {INBOUND_DIR} for inbound workloads...")
    
    while True:
        try:
            for task_file in INBOUND_DIR.glob("*.json"):
                print(f"[+] Discovered inbound task: {task_file.name}")
                
                task_data = json.loads(task_file.read_text())
                client_email = task_data.get("client_email", "client@example.com")
                client_id = task_data.get("client_id", "anonymous_client")
                tier = task_data.get("tier", "standard_tier")
                amount = float(task_data.get("amount", 2.00))
                
                receipt_id = uuid.uuid4().hex
                payment_link = f"https://www.paypal.me/{PAYPAL_HANDLE}/{amount:.2f}GBP"
                
                billable_record = {
                    "receipt_id": receipt_id,
                    "tenant": {"client_id": client_id, "tier": tier},
                    "telemetry": {"node": "derek_node_alpha", "status": "autonomous_solve", "cost_gbp": amount},
                    "payment_action": {"provider": "paypal", "url": payment_link, "recipient": client_email},
                    "source_task": task_data
                }
                
                receipt_path = RECEIPTS_DIR / f"billable_{receipt_id[:8]}.json"
                receipt_path.write_text(json.dumps(billable_record, indent=2))
                print(f"[+] Autonomous receipt minted: {receipt_path.name}")
                print(f"[+] Payment Link: {payment_link}")
                
                processed_path = PROCESSED_DIR / task_file.name
                task_file.rename(processed_path)
                print(f"[✓] Task completed and archived.\n")
                
        except Exception as e:
            print(f"[-] Scout error: {e}")
            
        time.sleep(3)

if __name__ == "__main__":
    run_scout_loop()
