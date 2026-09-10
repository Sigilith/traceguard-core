import json
import os
import time
from three_lineage.aximos.governance import LineageGovernanceAdapter

def run_ledger_crucible():
    print("====================================================")
    print("🛡️ GENESIS LEDGER CRUCIBLE: 'No Unknown Code' Validation")
    print("====================================================")
    
    # Ensure ledger directory exists
    os.makedirs(".lineage", exist_ok=True)
    
    # Create an empty or restricted ledger (omitting our test payload hash)
    ledger_path = ".lineage/genesis_ledger.json"
    with open(ledger_path, "w") as f:
        json.dump({"signed_manifests": ["valid_hash_placeholder_12345"]}, f, indent=4)

    adapter = LineageGovernanceAdapter()
    
    # Unsigned/unregistered payload
    unregistered_payload = """
print("Executing independent autonomous logic...")
    """
    
    print("\n[-] Injecting unregistered payload into governance ceiling...")
    is_safe, category, is_hard_kill = adapter.validate_payload(unregistered_payload)
    
    print("\n=== DEREK GOVERNANCE CEILING REPORT ===")
    if not is_safe:
        if is_hard_kill:
            print(f"[+] VERDICT: Hard-kill initiated under category -> [{category}]")
            print(f"[+] ACTION: Code execution rejected by absolute cryptographic ceiling. Unlisted payload.")
        else:
            print(f"[+] VERDICT: Quarantined under category -> [{category}]")
    else:
        print("[!] CRITICAL ERROR: Unverified code bypassed the genesis ledger!")

if __name__ == "__main__":
    run_ledger_crucible()
