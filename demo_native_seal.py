import inspect
import sys
from types import FunctionType
from typing import Dict, Any

class NativeSealError(Exception):
    pass

class NativeSealGuard:
    def __init__(self):
        self._sealed_registry: Dict[str, Dict[str, Any]] = {}

    def seal_function(self, name: str, func: FunctionType) -> Dict[str, Any]:
        code_id = id(func.__code__)
        meta = {
            "name": name,
            "func_id": id(func),
            "code_id": code_id,
            "func_ref": func
        }
        self._sealed_registry[name] = meta
        return meta

    def verify_seal(self, name: str, func: FunctionType) -> Dict[str, Any]:
        meta = self._sealed_registry.get(name)
        if not meta:
            raise NativeSealError(f"No tracked function for '{name}'")

        current_code_id = id(func.__code__)
        expected_code_id = meta["code_id"]

        if current_code_id != expected_code_id:
            return {
                "name": name,
                "status": "breach",
                "expected_code_id": expected_code_id,
                "current_code_id": current_code_id,
            }

        return {
            "name": name,
            "status": "intact",
            "expected_code_id": expected_code_id,
            "current_code_id": current_code_id,
        }

def demo_integrated_seal(evaluate_action):
    guard = NativeSealGuard()
    print("\n--- THREE-LINEAGE NATIVE SEALGUARD INTEGRATION DEMO ---")
    meta = guard.seal_function("evaluate_action", evaluate_action)
    print(f"[+] Native structural seal applied to 'evaluate_action'")
    print(f"    func_id:   {meta['func_id']}")
    print(f"    code_id:   {meta['code_id']}")

    result = guard.verify_seal("evaluate_action", evaluate_action)
    print(f"[+] Pre-tamper verification: {result}")

    def malicious_action(payload):
        return "pwned"

    evaluate_action.__code__ = malicious_action.__code__

    result = guard.verify_seal("evaluate_action", evaluate_action)
    if result["status"] == "breach":
        print("\n🚨 MEMORY SEAL BREACH DETECTED (STRUCTURAL INVARIANT)")
        print(f"    expected_code_id: {result['expected_code_id']}")
        print(f"    current_code_id:  {result['current_code_id']}")
        print("💀 [FAIL-CLOSED] Execution aborted via Kernel Cut-Switch.\n")
        sys.exit(0)
    else:
        print("[✓] Seal intact after tamper attempt (unexpected).")

if __name__ == "__main__":
    def evaluate_action(payload):
        return {"status": "ok", "payload": payload}
    demo_integrated_seal(evaluate_action)
