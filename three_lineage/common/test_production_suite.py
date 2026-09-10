import asyncio
import aiohttp

async def run_full_suite():
    BASE_URL = "http://127.0.0.1:8443"
    print("[*] Starting End-to-End Production Verification...")
    
    async with aiohttp.ClientSession() as session:
        # 1. Test Contract Issuance
        async with session.post(f"{BASE_URL}/v1/intent/contract", json={
            "issuer": {"agent_id": "derek-node-01"}, 
            "purpose": "Full Production Test"
        }) as resp:
            data = await resp.json()
            contract_id = data["result"]["contract_id"]
            print(f"[+] Contract Issued: {contract_id} (State: {data['result']['current_state']})")

        # 2. Test Intent Drift (Illegal Transition)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={
            "contract_id": contract_id,
            "transition": "execute_analysis",
            "code_payload": "10 + 10"
        }) as resp:
            res = await resp.json()
            print(f"[+] Intent Drift Intercepted: {res['api_status']} -> {res['audit_rationale']}")

        # 3. Test Step 1: S0 -> S1 (select_data)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={
            "contract_id": contract_id,
            "transition": "select_data",
            "code_payload": "8 * 8"
        }) as resp:
            res = await resp.json()
            print(f"[+] Step 1 Validated: {res['api_status']} (New State: {res['current_state']}, Result: {res['result']['result']})")

        # 4. Test Step 2: S1 -> S2 (execute_analysis)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={
            "contract_id": contract_id,
            "transition": "execute_analysis",
            "code_payload": "64 / 2"
        }) as resp:
            res = await resp.json()
            print(f"[+] Step 2 Validated: {res['api_status']} (New State: {res['current_state']}, Result: {res['result']['result']})")

if __name__ == "__main__":
    asyncio.run(run_full_suite())
