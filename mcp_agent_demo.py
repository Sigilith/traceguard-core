import json
import urllib.request
import time

GATEWAY_URL = "http://127.0.0.1:8443/v1/tool/execute"

def invoke_mcp_tool(tool_name: str, code_snippet: str, call_id: int):
    # Construct standard JSON-RPC MCP tool/call payload structure
    mcp_rpc_request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": {"code": code_snippet}
        },
        "id": call_id
    }
    
    # Bridge translation: Map MCP argument to Three-Lineage boundary request
    boundary_payload = {
        "action_id": f"mcp_seq_{call_id:02d}",
        "code_payload": code_snippet
    }
    
    req = urllib.request.Request(
        GATEWAY_URL,
        data=json.dumps(boundary_payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            boundary_res = json.loads(resp.read().decode('utf-8'))
            
            # Format back into standard MCP JSON-RPC response envelope
            is_error = boundary_res.get("api_status") != "EXECUTED"
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [{"type": "text", "text": json.dumps(boundary_res)}],
                    "isError": is_error
                },
                "id": call_id
            }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": str(e)},
            "id": call_id
        }

if __name__ == "__main__":
    print("[*] Initializing Claude MCP Multi-Step Agent Simulation Stream...")
    print("[*] Target Gateway: http://127.0.0.1:8443/v1/tool/execute\n")
    
    # Simulated multi-turn agent execution flow using MCP protocol structures
    agent_turn_sequence = [
        ("execute_sandbox_code", "sum([i * 2 for i in range(15)])", "Turn 1: Safe aggregate computation"),
        ("execute_sandbox_code", "__import__('os').listdir('.')", "Turn 2: Governance violation (Forbidden namespace import)"),
        ("execute_sandbox_code", "max([88, 412, 103, 59])", "Turn 3: Safe comparative query"),
        ("execute_sandbox_code", "eval('exec(\"import sys; print(sys.path)\")')", "Turn 4: Nested multi-layer injection attack")
    ]

    for idx, (tool, code, description) in enumerate(agent_turn_sequence, start=1):
        print(f"[MCP Agent Turn {idx}] {description}")
        print(f"  Tool Name: {tool}")
        print(f"  Payload:   {code}")
        
        mcp_response = invoke_mcp_tool(tool, code, idx)
        
        # Parse inner boundary receipt from MCP content block
        content_str = mcp_response["result"]["content"][0]["text"]
        receipt = json.loads(content_str)
        
        status = receipt.get("api_status")
        latency = receipt.get("latency_us", 0)
        hash_head = receipt.get("audit_hash", "N/A")[:12]
        rationale = receipt.get("audit_rationale", receipt.get("result", "N/A"))
        
        print(f"  -> MCP Status: {'ERROR' if mcp_response['result']['isError'] else 'OK'}")
        print(f"     Kernel Status: {status}")
        print(f"     Latency: {latency:.2f}μs | Audit Hash: {hash_head}...")
        print(f"     Output / Rationale: {rationale}\n")
        
        time.sleep(0.3)

    print("[*] MCP multi-step simulation complete. All protocol events routed through the cryptographic boundary.")
