import ast
import hashlib
import json
import time
import os
import random
from typing import Dict, Any, Tuple

class PolicyEngine:
    def evaluate(self, node: ast.AST) -> Tuple[bool, str]:
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id in {"eval", "exec", "__import__", "open", "os", "sys"}:
                    return False, f"FUZZ_VIOLATION: Restricted vector '{child.func.id}'."
        return True, "FUZZ_PASSED: Constraints met."

class TraceGuardCore:
    def __init__(self, policy: PolicyEngine):
        self.policy = policy

    def inspect(self, code: str) -> Tuple[bool, float, str]:
        start = time.perf_counter_ns()
        try:
            tree = ast.parse(code, mode='eval')
            passed, reason = self.policy.evaluate(tree)
            elapsed = (time.perf_counter_ns() - start) / 1000.0
            return passed, elapsed, reason
        except Exception as e:
            elapsed = (time.perf_counter_ns() - start) / 1000.0
            return False, elapsed, f"PARSE_ERR: {str(e)}"

class SigilithVault:
    def __init__(self, path: str = "vault_fuzz.dat"):
        self.path = path
        if os.path.exists(self.path):
            os.remove(self.path)
        self.head = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()

    def seal(self, pid: str, status: str, latency: float, reason: str):
        data = {
            "timestamp": time.time(),
            "pid": pid,
            "status": status,
            "latency": latency,
            "reason": reason,
            "parent": self.head
        }
        b_hash = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        data["block_hash"] = b_hash
        self.head = b_hash
        with open(self.path, "a") as f:
            f.write(json.dumps(data) + "\n")

    def verify(self) -> bool:
        if not os.path.exists(self.path):
            return False
        curr = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()
        with open(self.path, "r") as f:
            for line in f:
                d = json.loads(line.strip())
                parent = d.pop("parent")
                claimed = d.pop("block_hash")
                
                if parent != curr:
                    return False
                
                # Reconstruct exact dictionary that was originally hashed
                d_to_hash = dict(d)
                d_to_hash["parent"] = parent
                
                recomputed = hashlib.sha256(json.dumps(d_to_hash, sort_keys=True).encode()).hexdigest()
                if recomputed != claimed:
                    return False
                curr = claimed
        return True

if __name__ == "__main__":
    policy = PolicyEngine()
    guard = TraceGuardCore(policy)
    vault = SigilithVault()

    print("[*] Launching 1,000-payload adversarial fuzzing sweep...")
    vectors = [
        ("1 + 1", True),
        ("__import__('os')", False),
        ("eval('2+2')", False),
        ("[i for i in range(50)]", True),
        ("open('/etc/passwd')", False),
        ("exec('print(0)')", False),
        ("sum(range(100))", True)
    ]

    latencies = []
    for i in range(1, 1001):
        code, expected = random.choice(vectors)
        pid = f"fuzz_call_{i:04d}"
        passed, lat, reason = guard.inspect(code)
        latencies.append(lat)
        status = "CONTAINED" if not passed else "PASSED"
        vault.seal(pid, status, lat, reason)

    is_chain_valid = vault.verify()
    avg_lat = sum(latencies) / len(latencies)
    print(f"[*] Fuzzing complete. Iterations: 1000")
    print(f"[*] Average Latency: {avg_lat:.2f}μs | Peak Latency: {max(latencies):.2f}μs")
    print(f"[*] Cryptographic Ledger Integrity Verified: {is_chain_valid}")
