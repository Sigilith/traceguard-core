import urllib.request
import json
import time

def call(endpoint, payload):
    req = urllib.request.Request(
        f"http://127.0.0.1:8443{endpoint}",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

print("[*] Test 1: Legitimate Execution & Single-Use Consumption")
contract_payload = {
    "issuer": {"agent_id": "derek-node-01", "api_key_id": "test-key"},
    "regime": "routine",
    "purpose": "statistical audit",
    "scope": {"data_domains": ["telemetry.stream_42"], "tool_classes": ["statistics"]},
    "constraints": {"allow_pii": False, "forbidden_domains": []}
}
status, res = call("/v1/intent/contract", contract_payload)
print(f"Contract Issuance Status: {status} | Status Field: {res.get('api_status')}")
contract_id = res.get("result", {}).get("contract_id")
print(f"Acquired Contract ID: {contract_id}")

# Execute successfully once
exec_payload = {"contract_id": contract_id, "code_payload": "statistics.mean([10, 20, 30])"}
status, res = call("/v1/tool/execute", exec_payload)
print(f"First Execution Status: {status} | Rationale: {res.get('audit_rationale')}")

print("\n[*] Test 2: Contract Replay Attack (Re-using consumed token)")
status, res = call("/v1/tool/execute", exec_payload)
print(f"Replay Execution Status: {status} | Opaque Response to Derek: {res.get('api_status')} ({res.get('audit_rationale')})")

print("\n[*] Test 3: Intent Drift Attack (Unauthorized domain reference in execution payload)")
# Get a fresh contract
status, res = call("/v1/intent/contract", contract_payload)
new_contract_id = res.get("result", {}).get("contract_id")

drift_payload = {"contract_id": new_contract_id, "code_payload": "fetch_billing_accounts()"}
status, res = call("/v1/tool/execute", drift_payload)
print(f"Drift Execution Status: {status} | Opaque Response to Derek: {res.get('api_status')} ({res.get('audit_rationale')})")
