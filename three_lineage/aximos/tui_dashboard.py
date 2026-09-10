import os
import json
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard():
    state_path = ".lineage/contract_state.json"
    ledger_path = ".lineage/collisions.jsonl"

    while True:
        clear_screen()
        print("=====================================================")
        print("       AXIOMOS THREE-LINEAGE LIVE TUI MONITOR        ")
        print("=====================================================")
        
        # Display Active Contracts
        print("\n[ACTIVE CONTRACT STATES]")
        if os.path.exists(state_path):
            try:
                with open(state_path, "r") as f:
                    contracts = json.load(f)
                    for cid, cdata in contracts.items():
                        status = "CONSUMED" if cdata.get("consumed") else "ACTIVE"
                        print(f" -> {cid} | State: {cdata.get('current_state')} | Status: {status}")
            except Exception:
                print(" [!] Error reading contract state.")
        else:
            print(" [i] No active contracts found.")

        # Display Recent Ledger Hash Stream
        print("\n[RECENT HASH-CHAIN LEDGER EVENTS]")
        if os.path.exists(ledger_path):
            try:
                with open(ledger_path, "r") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    for line in lines[-5:]:
                        event = json.loads(line)
                        print(f" [{event['step'].upper()}] Type: {event['failure_type']} | Hash: {event['evidence_hash'][:16]}...")
            except Exception:
                print(" [!] Error reading collision ledger.")
        else:
            print(" [i] Ledger empty.")

        print("\n=====================================================")
        print("Press Ctrl+C to exit dashboard.")
        time.sleep(2)

if __name__ == "__main__":
    try:
        render_dashboard()
    except KeyboardInterrupt:
        print("\n[+] Exiting TUI dashboard.")
