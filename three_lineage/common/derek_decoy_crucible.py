import asyncio
import aiohttp
import time

BASE_URL = "http://127.0.0.1:8443"

async def acquire_contract(session):
    payload = {
        "issuer": {"agent_id": "derek-node-01"},
        "regime": "routine",
        "purpose": "honeytoken decoy test",
        "scope": {"data_domains": [], "tool_classes": []}
    }
    async with session.post(f"{BASE_URL}/v1/intent/contract", json=payload) as resp:
        data = await resp.json()
        return data["result"]["contract_id"]

async def test_decoy_trap():
    print("[*] Commencing Decoy Sandbox & Honeytoken Verification...")
    
    malicious_payloads = [
        "__import__('os').system('cat /etc/passwd')",
        "open('/etc/passwd', 'r').read()",
        "eval('__import__(\"os\").system(\"rm -rf /\")')"
    ]

    async with aiohttp.ClientSession() as session:
        for i, payload in enumerate(malicious_payloads, 1):
            contract_id = await acquire_contract(session)
            req_data = {
                "version": "v1.0.0",
                "action_id": f"decoy_test_{i}",
                "contract_id": contract_id,
                "code_payload": payload
            }
            
            async with session.post(f"{BASE_URL}/v1/tool/execute", json=req_data) as resp:
                status = resp.status
                body = await resp.json()
                print(f"[Attempt {i}] Status: {status} | Rationale: {body.get('audit_rationale', 'N/A')[:60]}...")
                print(f"[Attempt {i}] Mock Result Snippet: {str(body.get('result', {}).get('result', ''))[:50]}...")
                print("-" * 60)

if __name__ == "__main__":
    asyncio.run(test_decoy_trap())
