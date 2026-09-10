import asyncio
import aiohttp

async def test_fsm_governance():
    BASE_URL = "http://127.0.0.1:8443"
    async with aiohttp.ClientSession() as session:
        # 1. Issue Contract (Starts at S0_INTENT_DECLARED)
        async with session.post(f"{BASE_URL}/v1/intent/contract", json={"issuer": {"agent_id": "derek-node-01"}, "purpose": "FSM Trajectory Test"}) as resp:
            data = await resp.json()
            contract_id = data["result"]["contract_id"]
            print("Contract Initialized:", data)

        # 2. Test Illegal Transition Jump (Trying to jump straight to S2 analysis without S1 data selection)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={
            "contract_id": contract_id,
            "transition": "execute_analysis",
            "code_payload": "10 + 10"
        }) as resp:
            print("Illegal Transition Test (Intent Drift):", await resp.json())

        # 3. Execute Valid Step 1 (S0 -> S1 via select_data)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={
            "contract_id": contract_id,
            "transition": "select_data",
            "code_payload": "5 * 5"
        }) as resp:
            print("Valid Step 1 Execution:", await resp.json())

        # 4. Execute Valid Step 2 (S1 -> S2 via execute_analysis)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={
            "contract_id": contract_id,
            "transition": "execute_analysis",
            "code_payload": "100 / 4"
        }) as resp:
            print("Valid Step 2 Execution:", await resp.json())

if __name__ == "__main__":
    asyncio.run(test_fsm_governance())
