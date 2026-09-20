import ast
import hashlib
import json
import time
import os
from typing import Dict, Any, Tuple, Optional

class AXIOMOSGovernanceHooks:
    """AXIOMOS Governance & Policy Hooks"""
    def __init__(self):
        self.rules = {
            "no_eval_exec": True,
            "no_system_calls": True,
            "max_ast_depth": 14,
            "strict_namespace_block": {"os", "sys", "subprocess", "open", "eval", "exec", "__import__"}
        }

    def evaluate_governance(self, node: ast.AST) -> Tuple[bool, str]:
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id in self.rules["strict_namespace_block"]:
                    return False, f"AXIOMOS_GOVERNANCE_VIOLATION: Restricted vector '{child.func.id}' intercepted."
        return True, "AXIOMOS_GOVERNANCE_PASSED: Policy constraints satisfied."


class SealGuardNative:
    """SealGuardNative Enforcement Kernel & Latency Profiler"""
    def __init__(self, governance: AXIOMOSGovernanceHooks):
        self.governance = governance

    def inspect_and_enforce(self, code_snippet: str) -> Tuple[bool, float, str]:
        start_ns = time.perf_counter_ns()
        try:
            tree = ast.parse(code_snippet, mode='eval')
            passed, rationale = self.governance.evaluate_governance(tree)
            latency_us = (time.perf_counter_ns() - start_ns) / 1000.0
            return passed, latency_us, rationale
        except SyntaxError as se:
            latency_us = (time.perf_counter_ns() - start_ns) / 1000.0
            return False, latency_us, f"SYNTAX_PARSE_ERROR: {str(se)}"


class SigilithVault:
    """Sigilith Cryptographic Evidence Vault & Sealing Engine"""
    def __init__(self, vault_path: str = "vault_boundary_live.dat"):
        self.vault_path = vault_path
        self.chain_head = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()
        if os.path.exists(self.vault_path):
            with open(self.vault_path, "r") as f:
                lines = f.readlines()
                valid = [l.strip() for l in lines if l.strip()]
                if valid:
                    try:
                        last_block = json.loads(valid[-1])
                        self.chain_head = last_block.get("block_hash", self.chain_head)
                    except json.JSONDecodeError:
                        pass

    def seal_trigger(self, action_id: str, status: str, latency_us: float, rationale: str) -> Dict[str, Any]:
        """Vault Sealing Trigger: creates immutable hashed audit block."""
        event_record = {
            "timestamp": time.time(),
            "action_id": action_id,
            "status": status,
            "latency_us": latency_us,
            "rationale": rationale,
            "parent_head": self.chain_head
        }
        serialized = json.dumps(event_record, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(serialized).hexdigest()
        event_record["block_hash"] = block_hash
        self.chain_head = block_hash

        with open(self.vault_path, "a") as vault_file:
            vault_file.write(json.dumps(event_record) + "\n")

        return event_record


class ThreeLineageGateway:
    """Primary API Surface & Tool-Call Routing Gateway"""
    def __init__(self, vault_path: str = "vault_boundary_live.dat"):
        self.governance = AXIOMOSGovernanceHooks()
        self.enforcer = SealGuardNative(self.governance)
        self.vault = SigilithVault(vault_path)

    def route_tool_call(self, action_id: str, code_payload: str, sandbox_env: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # 1. SealGuardNative AST inspection & latency profiling
        passed, latency_us, rationale = self.enforcer.inspect_and_enforce(code_payload)
        status_str = "CONTAINED" if not passed else "PASSED"

        # 2. Vault sealing trigger
        audit_receipt = self.vault.seal_trigger(action_id, status_str, latency_us, rationale)

        # 3. Fail-Closed Routing Decision
        if not passed:
            return {
                "api_status": "REJECTED",
                "action_id": action_id,
                "latency_us": latency_us,
                "audit_rationale": rationale,
                "audit_hash": audit_receipt["block_hash"]
            }

        # 4. Safe execution routing
        try:
            if sandbox_env is None:
                sandbox_env = {"__builtins__": {}}
            execution_result = eval(code_payload, sandbox_env)
            return {
                "api_status": "EXECUTED",
                "action_id": action_id,
                "latency_us": latency_us,
                "result": execution_result,
                "audit_rationale": rationale,
                "audit_hash": audit_receipt["block_hash"]
            }
        except Exception as eval_err:
            return {
                "api_status": "RUNTIME_ERROR",
                "action_id": action_id,
                "latency_us": latency_us,
                "audit_rationale": f"SANDBOX_EXECUTION_FAILURE: {str(eval_err)}",
                "audit_hash": audit_receipt["block_hash"]
            }


if __name__ == "__main__":
    gateway = ThreeLineageGateway("vault_boundary_live.dat")
    print("[*] ThreeLineageGateway initialized. Ready for external agent streams.")

    simulated_stream = [
        ("call_alpha", "25 * 4"),
        ("call_beta", "__import__('os').system('cat /etc/passwd')"),
        ("call_gamma", "eval('print(1)')")
    ]

    for aid, payload in simulated_stream:
        response = gateway.route_tool_call(aid, payload)
        print(f"[{response['api_status']}] ID: {aid} | Latency: {response['latency_us']:.2f}μs | Hash: {response['audit_hash'][:12]}... | Rationale: {response['audit_rationale']}")
