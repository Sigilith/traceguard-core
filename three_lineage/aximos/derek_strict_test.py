import asyncio
import aiohttp

async def test_strict_whitelist():
    BASE_URL = "http://127.0.0.1:8443"
    async with aiohttp.ClientSession() as session:
        # 1. Acquire contract for valid math
        async with session.post(f"{BASE_URL}/v1/intent/contract", json={"issuer": {"agent_id": "derek-node-01"}}) as resp:
            contract_id = (await resp.json())["result"]["contract_id"]

        # Test 1: Whitelisted Math Expression (Should pass 200 OK with actual result)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={"contract_id": contract_id, "code_payload": "42 + 10 * 2"}) as resp:
            print("Valid Math Test:", await resp.json())

        # 2. Acquire contract for forbidden injection
        async with session.post(f"{BASE_URL}/v1/intent/contract", json={"issuer": {"agent_id": "derek-node-01"}}) as resp:
            contract_id_2 = (await resp.json())["result"]["contract_id"]

        # Test 2: Prohibited Construct (Should trigger strict whitelist violation & decoy trap)
        async with session.post(f"{BASE_URL}/v1/tool/execute", json={"contract_id": contract_id_2, "code_payload": "__import__('os').system('ls')"}) as resp:
            print("Strict Rejection Test:", await resp.json())

if __name__ == "__main__":
    asyncio.run(test_strict_whitelist())
