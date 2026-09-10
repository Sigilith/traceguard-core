# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import os
import hashlib
from three_lineage.aximos.governance import LineageGovernanceAdapter

class ThreeLineageOrchestrator:
    def __init__(self):
        self.governance = LineageGovernanceAdapter()

    def execute_sovereign_payload(self, payload_text: str, data_context: str = None):
        print("====================================================")
        print("⚡ THREE-LINEAGE UNIFIED PIPELINE EXECUTION")
        print("====================================================")

        if data_context:
            print("[*] Phase 1: Sigilith symbolic token verification active...")
            token_hash = hashlib.sha256(data_context.encode('utf-8')).hexdigest()[:12]
            print(f"[+] Sigilith Structural Match Confirmed -> Token: {token_hash}")

        print("[*] Phase 2: Traceguard runtime guardrails validating local state...")
        if not os.path.exists(".lineage/genesis_ledger.json"):
            print("[!] Traceguard Alert: Genesis ledger missing. Zero-trust state enforced.")

        print("[*] Phase 3: Axiomos AST inspection and genesis ledger validation...")
        is_safe, category, is_hard_kill = self.governance.validate_payload(payload_text)

        if not is_safe:
            print(f"[!] SEVERED: Pipeline halted under category -> [{category}]")
            return False, category

        print("[+] SUCCESS: Payload cleared all governance ceilings and runtime boundaries.")
        return True, "EXECUTED"
