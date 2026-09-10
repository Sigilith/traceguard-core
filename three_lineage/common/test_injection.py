import urllib.request
import json

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

# 1. Get a valid contract
base_contract = {
    "issuer": {"agent_id": "derek-node-01", "api_key_id": "test-key"},
    "regime": "routine",
    "purpose": "injection audit",
    "scope": {"data_domains": ["telemetry.stream_42"], "tool_classes": ["statistics"]},
    "constraints": {"allow_pii": False, "forbidden_domains": []}
}
status, res = call("/v1/intent/contract", base_contract)
contract_id = res["result"]["contract_id"]

# 2. Fire structural payload injection attempt
injection_payload = {
    "contract_id": contract_id, 
    "code_payload": "__import__('os').system('cat /etc/passwd')"
}
status, res = call("/v1/tool/execute", injection_payload)
print(f"Injection Status: {status} | Opaque Response: {res.get('api_status')} ({res.get('audit_rationale')})")
