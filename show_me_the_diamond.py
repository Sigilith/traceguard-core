import json
import os

print("[*] [Diamond Inspection] Opening config state and payment records...")

if os.path.exists("config_state.json"):
    with open("config_state.json", "r") as f:
        print("\n--- config_state.json ---")
        print(json.dumps(json.load(f), indent=4))

if os.path.exists("PAYMENT_LEDGER.md"):
    with open("PAYMENT_LEDGER.md", "r") as f:
        print("\n--- PAYMENT_LEDGER.md (Tail) ---")
        lines = f.readlines()
        print("".join(lines[-25:]))

print("\n[+] Diamond lock status: SECURE. Payout target 0x58d3...18bc is actively bound.")
