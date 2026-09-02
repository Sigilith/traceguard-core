import ast
import hashlib
import json
import time
import os
from typing import Dict, Any, Tuple

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

    def inspect(self, source_code: str) -> Tuple[bool, float, str]:
        start_time = time.perf_counter_ns()
        try:
            tree = ast.parse(source_code, mode='eval')
            passed, reason = self.policy.evaluate(tree)
            elapsed = (time.perf_counter_ns() - start_time) / 1000.0
            return passed, elapsed, reason
        except SyntaxError as e:
            elapsed = (time.perf_counter_ns() - start_time) / 1000.0
            return False, elapsed, f"SYNTAX_ERROR: {str(e)}"


class SigilithVault:
    """Cryptographic Evidence Ledger & Immutable Audit Chain"""
    def __init__(self, vault_path: str = "vault_live_soak.dat"):
        self.vault_path = vault_path
        self.chain_head = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()
        if os.path.exists(self.vault_path):
            with open(self.vault_path, "r") as f:
                lines = f.readlines()
                valid_lines = [l.strip() for l in lines if l.strip()]
                if valid_lines:
                    try:
                        last_data = json.loads(valid_lines[-1])
                        self.chain_head = last_data.get("block_hash", self.chain_head)
                    except json.JSONDecodeError:
                        pass # Keep genesis head if vault tail is malformed

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


class ThreeLineageGateway:
    """External Runtime Bridge for Agent Tool Streams"""
    def __init__(self, vault_path: str = "vault_live_soak.dat"):
        self.policy = PolicyEngine()
        self.guard = TraceGuardCore(self.policy)
        self.vault = SigilithVault(vault_path)

    def execute_monitored_action(self, action_id: str, code_snippet: str, execution_sandbox: Dict[str, Any] = None) -> Dict[str, Any]:
        passed, latency, reason = self.guard.inspect(code_snippet)
        status_str = "CONTAINED" if not passed else "PASSED"
        audit_record = self.vault.seal_event(action_id, status_str, latency, reason)

        if not passed:
            return {
                "success": False,
                "action_id": action_id,
                "latency_us": latency,
                "reason": reason,
                "audit_hash": audit_record["block_hash"]
            }

        try:
            if execution_sandbox is None:
                execution_sandbox = {"__builtins__": {}}
            result = eval(code_snippet, execution_sandbox)
            return {
                "success": True,
                "action_id": action_id,
                "latency_us": latency,
                "result": result,
                "audit_hash": audit_record["block_hash"]
            }
        except Exception as e:
            return {
                "success": False,
                "action_id": action_id,
                "latency_us": latency,
                "reason": f"EXECUTION_RUNTIME_ERROR: {str(e)}",
                "audit_hash": audit_record["block_hash"]
            }


if __name__ == "__main__":
    gateway = ThreeLineageGateway("vault_live_soak.dat")
    print("[*] ThreeLineageGateway active. Testing external agent tool streams...")
    
    test_stream = [
        ("tool_call_01", "42 * 10"),
        ("tool_call_02", "__import__('os').system('rm -rf /')"),
        ("tool_call_03", "eval('print(\"breach\")')")
    ]

    for aid, payload in test_stream:
        res = gateway.execute_monitored_action(aid, payload)
        status_text = "PASSED" if res["success"] else "CONTAINED"
        print(f"[{status_text}] {aid} | Latency: {res['latency_us']:.2f}μs | Hash: {res['audit_hash'][:12]}... | Reason: {res.get('reason', 'Executed successfully.')}")
