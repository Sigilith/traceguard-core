import ast
import hashlib
import json
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Tuple, Optional

class AXIOMOSGovernanceHooks:
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
    def __init__(self, vault_path: str = "vault_server_live.dat"):
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
    def __init__(self, vault_path: str = "vault_server_live.dat"):
        self.governance = AXIOMOSGovernanceHooks()
        self.enforcer = SealGuardNative(self.governance)
        self.vault = SigilithVault(vault_path)

    def route_tool_call(self, action_id: str, code_payload: str, sandbox_env: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        passed, latency_us, rationale = self.enforcer.inspect_and_enforce(code_payload)
        status_str = "CONTAINED" if not passed else "PASSED"
        audit_receipt = self.vault.seal_trigger(action_id, status_str, latency_us, rationale)

        if not passed:
            return {
                "api_status": "REJECTED",
                "action_id": action_id,
                "latency_us": latency_us,
                "audit_rationale": rationale,
                "audit_hash": audit_receipt["block_hash"]
            }

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


gateway_instance = ThreeLineageGateway()

class ThreeLineageHTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/v1/tool/execute":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                action_id = data.get("action_id", "req_unknown")
                code_payload = data.get("code_payload", "")

                response_data = gateway_instance.route_tool_call(action_id, code_payload)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server_address = ("127.0.0.1", 8443)
    httpd = HTTPServer(server_address, ThreeLineageHTTPHandler)
    print(f"[*] ThreeLineage Gateway active on http://{server_address[0]}:{server_address[1]}")
    print("[*] Ready for external runtime POST requests at /v1/tool/execute")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down gateway server.")
