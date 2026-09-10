import json
import uuid
from pathlib import Path

RECEIPTS_DIR = Path(".lineage/derek_receipts")

def generate_billable_receipt(client_id: str, tier: str, payload_data: dict, unit_cost: float = 0.001):
    if not RECEIPTS_DIR.exists():
        RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
        
    receipt_id = uuid.uuid4().hex
    
    billable_record = {
        "receipt_id": receipt_id,
        "tenant": {
            "client_id": client_id,
            "tier": tier
        },
        "telemetry": {
            "node": "derek_node_alpha",
            "status": "verified",
            "units_consumed": 1,
            "estimated_cost_gbp": unit_cost
        },
        "payload": payload_data
    }
    
    file_path = RECEIPTS_DIR / f"billable_{receipt_id[:8]}.json"
    file_path.write_text(json.dumps(billable_record, indent=2))
    print(f"[+] Generated billable receipt for {client_id} [{tier}]: {file_path.name}")
    return file_path

if __name__ == "__main__":
    generate_billable_receipt(
        client_id="acme_corp_01",
        tier="enterprise_tier",
        payload_data={"event": "containment_checkpoint_cleared", "hash": "cf96640fc155"}
    )
