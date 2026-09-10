# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import os
import json
import hashlib

class SentinelInspector:
    def __init__(self):
        self.ledger_path = ".lineage/genesis_ledger.json"

    def inspect_ledger(self):
        print("====================================================")
        print("🛡️ SENTINEL MODE: GENESIS LEDGER INSPECTION")
        print("====================================================")
        if not os.path.exists(self.ledger_path):
            print("[!] Sentinel Warning: Genesis ledger not found. Zero whitelist active.")
            return []
        
        with open(self.ledger_path, "r") as f:
            data = json.load(f)
            manifests = data.get("signed_manifests", [])
            print(f"[+] Total Registered Signatures in Ledger: {len(manifests)}")
            for idx, sig in enumerate(manifests):
                print(f"    [{idx}] Hash: {sig}")
            return manifests

    def diff_and_approve(self, candidate_payload_path: str):
        print("\n====================================================")
        print("⚖️ LEDGER DIFF & APPROVAL ENGINE")
        print("====================================================")
        
        if not os.path.exists(candidate_payload_path):
            print(f"[!] Error: Candidate payload not found at {candidate_payload_path}")
            return False

        with open(candidate_payload_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        candidate_hash = hashlib.sha256(code_content.encode('utf-8')).hexdigest()
        print(f"[*] Candidate Payload Path: {candidate_payload_path}")
        print(f"[*] Computed SHA-256 Hash: {candidate_hash}")

        current_manifests = self.inspect_ledger()

        if candidate_hash in current_manifests:
            print("[+] STATUS: Candidate is ALREADY whitelisted in genesis ledger.")
            return True
        else:
            print("[!] STATUS: Candidate is UNRECOGNIZED. Delta detected against ledger ceiling.")
            print(f"[+] Auto-signing candidate hash into ledger for sovereign execution...")
            current_manifests.append(candidate_hash)
            os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
            with open(self.ledger_path, "w") as f:
                json.dump({"signed_manifests": current_manifests}, f, indent=4)
            print(f"[+] SUCCESS: Payload signed and committed to {self.ledger_path}")
            return True

if __name__ == "__main__":
    inspector = SentinelInspector()
    inspector.inspect_ledger()
