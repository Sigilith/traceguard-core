import subprocess
import json
import sys

def test_mcp_bridge():
    print("[*] Spawning Three-Lineage MCP Bridge process...")
    
    # Start the MCP server process
    process = subprocess.Popen(
        ["python3", "three_lineage_mcp.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Standard MCP initialization handshake payload
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "Termux-Harness", "version": "1.0.0"}
        },
        "id": 1
    }

    # Tool call request payload (Safe execution)
    tool_request_safe = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "secure_execute",
            "arguments": {"code": "sum([5, 10, 15, 20])"}
        },
        "id": 2
    }

    # Tool call request payload (Governance violation)
    tool_request_violation = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "secure_execute",
            "arguments": {"code": "__import__('os').system('ls')"}
        },
        "id": 3
    }

    # Send initialization and test calls
    payloads = [init_request, tool_request_safe, tool_request_violation]
    
    for p in payloads:
        out_str = json.dumps(p) + "\n"
        process.stdin.write(out_str)
        process.stdin.flush()
        
    # Read responses with a short delay for stdout flushing
    import time
    time.sleep(1)
    
    process.terminate()
    stdout_data, stderr_data = process.communicate()
    
    print("\n--- MCP SERVER STDOUT ---")
    print(stdout_data)
    if stderr_data:
        print("\n--- MCP SERVER STDERR ---")
        print(stderr_data)

if __name__ == "__main__":
    test_mcp_bridge()
