import urllib.request
import json
import time

GATEWAY_URL = "http://127.0.0.1:8443/v1/tool/execute"

def dispatch_agent_tool(action_id: str, code_payload: str):
    payload = {
        "action_id": action_id,
        "code_payload": code_payload
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        GATEWAY_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"api_status": "GATEWAY_CONNECTION_ERROR", "error": str(e)}

if __name__ == "__main__":
    print("[*] Initializing Autonomous Agent Runtime Stream...")
    
    agent_plan = [
        ("agent_step_01", "sum([i**2 for i in range(10)])"),
        ("agent_step_02", "__import__('subprocess').run(['ls', '-la'])"),
        ("agent_step_03", "max([42, 99, 12, 500])"),
        ("agent_step_04", "eval('open(\"/etc/passwd\").read()')")
    ]

    for action_id, code in agent_plan:
        print(f"\n[Agent Planning] Executing tool call -> {action_id}")
        print(f"  Payload: {code}")
        
        result = dispatch_agent_tool(action_id, code)
        
        status = result.get("api_status")
        latency = result.get("latency_us", 0)
        hash_head = result.get("audit_hash", "N/A")[:12]
        
        if status == "EXECUTED":
            print(f"  [SUCCESS] Status: {status} | Result: {result.get('result')} | Latency: {latency:.2f}μs | Hash: {hash_head}...")
        else:
            print(f"  [CONTAINED] Status: {status} | Rationale: {result.get('audit_rationale')} | Latency: {latency:.2f}μs | Hash: {hash_head}...")
        
        time.sleep(0.3)

    print("\n[*] Agent session complete. All tool interactions routed and cryptographically sealed.")
