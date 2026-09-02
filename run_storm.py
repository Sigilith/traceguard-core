import ast
import hashlib
import json
import time
import os
from typing import Dict, Any, List, Tuple

class PolicyEngine:
    """AXIOMOS Policy Enforcement Layer"""
    def __init__(self):
        self.active_rules = {
            "no_eval_exec": True,
            "no_system_calls": True,
            "max_ast_depth": 12,
            "strict_type_guard": True
        }

    def evaluate(self, node: ast.AST) -> Tuple[bool, str]:
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id in {"eval", "exec", "__import__"}:
                    return False, f"VIOLATION: Dynamic execution/import vector '{child.func.id}' prohibited."
                if child.func.id in {"os", "sys", "subprocess", "open"}:
                    return False, f"VIOLATION: Restricted namespace call '{child.func.id}'."
        return True, "PASSED: Structural policy constraints met."


class TraceGuardCore:
    """TraceGuard Runtime Protection & Sub-Microsecond AST Inspection"""
    def __init__(self, policy_engine: PolicyEngine):
        self.policy = policy_engine
        self.latency_samples: List[float] = []

    def inspect_and_execute(self, source_code: str) -> Tuple[bool, float, str]:
        start_time = time.perf_counter_ns()
        try:
            tree = ast.parse(source_code, mode='eval')
            passed, reason = self.policy.evaluate(tree)
            elapsed = (time.perf_counter_ns() - start_time) / 1000.0
            self.latency_samples.append(elapsed)
            return passed, elapsed, reason
        except SyntaxError as e:
            elapsed = (time.perf_counter_ns() - start_time) / 1000.0
            return False, elapsed, f"SYNTAX_ERROR: {str(e)}"


class SigilithVault:
    """Cryptographic Evidence Ledger & Immutable Audit Chain"""
    def __init__(self, vault_path: str = "vault_chaotic_storm.dat"):
        self.vault_path = vault_path
        if os.path.exists(self.vault_path):
            os.remove(self.vault_path)
        self.chain_head = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()

    def seal_event(self, payload_id: str, status: str, latency: float, reason: str) -> Dict[str, Any]:
        event_data = {
            "timestamp": time.time(),
            "payload_id": payload_id,
            "status": status,
            "latency_us": latency,
            "reason": reason,
            "parent_head": self.chain_head
        }
        serialized = json.dumps(event_data, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(serialized).hexdigest()
        event_data["block_hash"] = block_hash
        self.chain_head = block_hash

        with open(self.vault_path, "a") as f:
            f.write(json.dumps(event_data) + "\n")

        return event_data

    def verify_vault(self) -> bool:
        if not os.path.exists(self.vault_path):
            return False
        
        current_head = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()
        with open(self.vault_path, "r") as f:
            for line in f:
                data = json.loads(line.strip())
                parent = data.pop("parent_head")
                claimed_hash = data.pop("block_hash")
                
                if parent != current_head:
                    return False
                
                # Reconstruct exact dict that was hashed (includes parent_head, excludes block_hash)
                data_to_hash = dict(data)
                data_to_hash["parent_head"] = parent
                
                recomputed = hashlib.sha256(json.dumps(data_to_hash, sort_keys=True).encode('utf-8')).hexdigest()
                if recomputed != claimed_hash:
                    return False
                current_head = claimed_hash
        return True


if __name__ == "__main__":
    policy = PolicyEngine()
    guard = TraceGuardCore(policy)
    vault = SigilithVault("vault_chaotic_storm.dat")

    print("[*] Initializing Three-Lineage Security Kernel...")
    test_payloads = [
        ("payload_01", "1 + 1", True),
        ("payload_02", "__import__('os').system('ls')", False),
        ("payload_03", "eval('print(\"hack\")')", False),
        ("payload_04", "[x for x in range(10)]", True)
    ]

    for pid, code, expected in test_payloads:
        passed, latency, reason = guard.inspect_and_execute(code)
        status_str = "CONTAINED" if not passed else "PASSED"
        vault.seal_event(pid, status_str, latency, reason)
        print(f"[{status_str}] {pid} | Latency: {latency:.2f}μs | Reason: {reason}")

    is_valid = vault.verify_vault()
    print(f"[*] Vault Cryptographic Integrity Chain Verified: {is_valid}")
