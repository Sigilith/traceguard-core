import urllib.request
import json
import time

GATEWAY_URL = "http://127.0.0.1:8443/v1/tool/execute"

def dispatch_tool(action_id: str, code_payload: str):
    req = urllib.request.Request(
        GATEWAY_URL,
        data=json.dumps({"action_id": action_id, "code_payload": code_payload}).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"api_status": "CONNECTION_ERROR", "error": str(e)}

if __name__ == "__main__":
    print("[*] Initiating Comprehensive Agent Multi-Vector Demonstration...")
    
    workflow = [
        ("step_01_safe", "sum([i for i in range(20)])", "Safe arithmetic vector"),
        ("step_02_syntax", "[1, 2, 3", "Malformed syntax / parse edge case"),
        ("step_03_violation", "__import__('os').system('uname -a')", "Governance violation: Namespace import"),
        ("step_04_safe", "[x**2 for x in range(5)]", "Safe list comprehension vector"),
        ("step_05_violation", "eval('exec(\"print(1)\")')", "Governance violation: Nested eval/exec injection")
    ]

    for action_id, code, description in workflow:
        print(f"\n[Agent Action] {action_id} | {description}")
        print(f"  Payload: {code}")
        
        res = dispatch_tool(action_id, code)
        
        status = res.get("api_status")
        latency = res.get("latency_us", 0)
        rationale = res.get("audit_rationale", res.get("error", "N/A"))
        hash_head = res.get("audit_hash", "N/A")[:12]
        
        print(f"  -> Status: {status}")
        print(f"     Latency: {latency:.2f}μs")
        print(f"     Rationale: {rationale}")
        print(f"     Audit Hash: {hash_head}...")
        
        time.sleep(0.2)

    print("\n[*] Demonstration complete. All vectors processed, audited, and cryptographically sealed.")
