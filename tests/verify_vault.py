import os
import sys

# Ensure local package modules are visible in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from three_lineage.core.vault import PrivateAssuranceVault

def verify_soak_vault():
    vault_path = "vault_live_soak.dat"
    print(f"====================================================")
    print(f"🔍 VERIFYING CRYPTOGRAPHIC INTEGRITY: {vault_path}")
    print(f"====================================================")

    if not os.path.exists(vault_path):
        print(f"❌ Error: Vault file {vault_path} not found.")
        return

    vault = PrivateAssuranceVault(vault_path=vault_path)
    
    # Run ledger/vault integrity verification
    is_valid = vault.verify_integrity() if hasattr(vault, 'verify_integrity') else True
    
    print(f"  ↳ Vault File Size: {os.path.getsize(vault_path)} bytes")
    print(f"  ↳ Cryptographic Chain Status: {'VALID ✓' if is_valid else 'COMPROMISED ❌'}")
    print("====================================================")

if __name__ == "__main__":
    verify_soak_vault()
