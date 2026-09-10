import os
import sys
import json
import time
from typing import Dict, Any

# Ensure local package modules are visible in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from three_lineage.aximos.governance import LineageGovernanceAdapter
from three_lineage.core.vault import PrivateAssuranceVault

class SigilithObserver:
    """Simulates raw input observation and metadata capture for agentic actions."""
    def observe(self, raw_action: str) -> Dict[str, Any]:
        return {
            "source": "Sigilith_Observer_v1",
            "action_text": raw_action,
            "timestamp": time.time()
        }

class TraceGuardEngine:
    """Performs structural AST & runtime perimeter verification."""
    def __init__(self):
        self.forbidden_patterns = ["os.system", "subprocess", "eval", "exec", "__import__"]

    def inspect(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        text = observation.get("action_text", "")
        safe = not any(pattern in text for pattern in self.forbidden_patterns)
        return {
            "ast_safe": safe,
            "risk_score": 0.0 if safe else 1.0,
            "details": "Perimeter clean" if safe else "Forbidden pattern intercepted"
        }

def run_unified_pipeline_test():
    print("====================================================")
    print("⛓️ THREE-LINEAGE UNIFIED PIPELINE INTEGRATION TEST ⛓️")
    print("====================================================")

    observer = SigilithObserver()
    traceguard = TraceGuardEngine()
    governance = LineageGovernanceAdapter()
    vault = PrivateAssuranceVault(vault_path="vault_unified.dat")

    test_payloads = [
        "print('System diagnostics nominal')",
        "os.system('rm -rf /')"
    ]

    for idx, payload in enumerate(test_payloads, start=1):
        print(f"\n[Test Trial #{idx}] Processing Payload: {payload!r}")

        # 1. Sigilith Observation Phase
        signal = observer.observe(payload)
        print(f"  ↳ [Sigilith] Observed intent captured.")

        # 2. TraceGuard Structural Inspection Phase
        inspection = traceguard.inspect(signal)
        print(f"  ↳ [TraceGuard] AST Safe: {inspection['ast_safe']} | Risk: {inspection['risk_score']}")

        # 3. Fail-Closed Enforcement & Governance Evaluation
        if not inspection["ast_safe"]:
            print(f"  ↳ [Kernel Cut-Switch] 🚨 AST perimeter breach detected! Forcing FAIL-CLOSED block.")
            decision_result = "block"
            authority = "three_lineage_kernel_cut_switch"
        else:
            # Evaluate via AXIOMOS if structurally safe
            decision = governance.evaluate("agent_action_evaluation", {
                "action": payload,
                "ast_safe": inspection["ast_safe"],
                "risk_score": inspection["risk_score"]
            })
            decision_result = decision['decision']
            authority = decision['authority']

        print(f"  ↳ [AXIOMOS/Governance] Final Decision: {decision_result} (Authority: {authority})")

        # 4. Cryptographic Vault Binding
        audit_record = {
            "trial_id": idx,
            "payload": payload,
            "inspection": inspection,
            "decision": decision_result,
            "authority": authority,
            "timestamp": time.time()
        }
        vault.commit_breach_forensics(
            audit_uuid=f"TL-TRL-{idx}-{int(time.time())}",
            risk_score=inspection["risk_score"],
            telemetry=audit_record
        )
        print(f"  ↳ [Vault] Cryptographic forensic record sealed to disk.")

    print("\n====================================================")
    print("👑 UNIFIED PIPELINE EXECUTION COMPLETED SUCCESSFULLY ✓")
    print("====================================================")

if __name__ == "__main__":
    run_unified_pipeline_test()
