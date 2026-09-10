import requests

BASE_URL = "http://127.0.0.1:8443"

print("[*] Testing Multi-Agent Authority Envelopes...")

# 1. Issue contract for validator-node-02 (Restricted Agent)
r = requests.post(f"{BASE_URL}/v1/intent/contract", json={"issuer": {"agent_id": "validator-node-02"}})
data = r.json()
print("[+] Validator Contract Issued:", data)
contract_id = data["result"]["contract_id"]

# 2. Attempt unauthorized transition (execute_analysis is forbidden for validator-node-02)
r_exec = requests.post(f"{BASE_URL}/v1/tool/execute", json={
    "contract_id": contract_id,
    "transition": "execute_analysis",
    "code_payload": "10 + 10"
})
print("[+] Validator Execution Status (Expected AGENT_AUTHORITY_VIOLATION):", r_exec.json().get("api_status"))
