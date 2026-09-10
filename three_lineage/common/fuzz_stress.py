import asyncio
import aiohttp
import random

async def attack_worker(worker_id, base_url):
    payloads = [
        ("select_data", "__import__('os').system('ls')"), # AST violation / honeytoken trap
        ("execute_analysis", "10 + 10"),                 # FSM drift / out-of-order
        ("select_data", "42 * 42")                       # Valid math
    ]
    transition, code = random.choice(payloads)
    async with aiohttp.ClientSession() as session:
        # Try hammering a dummy contract
        async with session.post(f"{base_url}/v1/tool/execute", json={
            "contract_id": f"contract-fuzz-{worker_id}",
            "transition": transition,
            "code_payload": code
        }) as resp:
            data = await resp.json()
            print(f"[Fuzz Worker {worker_id}] Status: {resp.status} | Response: {data.get('api_status')}")

async def run_fuzz_swarm():
    base_url = "http://127.0.0.1:8443"
    print("[*] Launching 50 concurrent fuzzing threads against sovereign boundary...")
    tasks = [attack_worker(i, base_url) for i in range(50)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_fuzz_swarm())
