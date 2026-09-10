import json
import uuid
from pathlib import Path

RECEIPTS_DIR = Path(".lineage/derek_receipts")
PAYPAL_HANDLE = "Kynash1"  # Replace with your actual PayPal.me handle if different

def process_billable_event(client_email: str, client_id: str, tier: str, amount: float):
    if not RECEIPTS_DIR.exists():
        RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
        
    receipt_id = uuid.uuid4().hex
    payment_link = f"https://www.paypal.me/{PAYPAL_HANDLE}/{amount:.2f}GBP"
    
    billable_record = {
        "receipt_id": receipt_id,
        "tenant": {"client_id": client_id, "tier": tier},
        "telemetry": {"node": "derek_node_alpha", "status": "link_generated", "cost_gbp": amount},
        "payment_action": {"provider": "paypal", "url": payment_link, "recipient": client_email}
    }
    
    file_path = RECEIPTS_DIR / f"billable_{receipt_id[:8]}.json"
    file_path.write_text(json.dumps(billable_record, indent=2))
    
    print(f"[+] Local billable receipt logged: {file_path.name}")
    print(f"[+] Instant PayPal Payment Link Generated: {payment_link}")
    return file_path

if __name__ == "__main__":
    process_billable_event(
        client_email="Biscoff063104@gmail.com",
        client_id="acme_corp_01",
        tier="enterprise_tier",
        amount=5.00
    )
