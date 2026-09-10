import json
import time
from pathlib import Path

def load_last_vault_event():
    ledger_path = Path("traceguard_async_ledger.jsonl")
    if not ledger_path.exists():
        return "No ledger events recorded."
    lines = ledger_path.read_text(encoding="utf-8").strip().split("\n")
    if not lines:
        return "Ledger empty."
    try:
        last = json.loads(lines[-1])
        return f"{last.get('event')} (task {last.get('task_id')})"
    except:
        return "Ledger unreadable."

def load_lineage_head():
    head_path = Path("three_lineage/lineage_head.txt")
    if not head_path.exists():
        return "No lineage head."
    return head_path.read_text(encoding="utf-8").strip()

def print_banner():
    print("\n===================================================")
    print("        THREE-LINEAGE SOVEREIGN RUNTIME")
    print("===================================================")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Lineage Head: {load_lineage_head()}")
    print(f"Last Vault Event: {load_last_vault_event()}")
    print("Environment: ./three-lineage-core")
    print("===================================================\n")

if __name__ == '__main__':
    print_banner()
