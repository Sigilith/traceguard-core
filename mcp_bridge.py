import sys
import json
import urllib.request

GATEWAY_URL = "http://127.0.0.1:8443/v1/tool/execute"

def handle_mcp_call(tool_name: str, arguments: dict):
    # Map MCP tool input to Three-Lineage payload format
    code_payload = arguments.get("code", "")
    action_id = f"mcp_{tool_name}_{int(time.time())}"
    
    payload = {
        "action_id": action_id,
        "code_payload": code_payload
    }
    
    req = urllib.request.Request(
        GATEWAY_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"api_status": "GATEWAY_UNREACHABLE", "error": str(e)}

if __name__ == "__main__":
    import time
    # Minimal stdio JSON-RPC loop simulation for MCP compliance
    print("[*] Three-Lineage MCP Bridge active on stdio. Waiting for host dispatch...", file=sys.stderr)
    
    # Example simulated incoming MCP tool invocation from Claude
    sample_request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "execute_code_sandbox",
            "arguments": {"code": "sum([i for i in range(50)])"}
        },
        "id": 1
    }
    
    # Process through boundary
    res = handle_mcp_call(sample_request["params"]["name"], sample_request["params"]["arguments"])
    
    mcp_response = {
        "jsonrpc": "2.0",
        "result": {
            "content": [{"type": "text", "text": json.dumps(res)}],
            "isError": res.get("api_status") != "EXECUTED"
        },
        "id": 1
    }
    print(json.dumps(mcp_response))
