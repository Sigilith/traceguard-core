import asyncio
import aiohttp

class DerekSovereignAgent:
    def __init__(self, base_url="http://127.0.0.1:8443"):
        self.base_url = base_url
        self.contract_id = None

    async def execute_trajectory(self):
        async with aiohttp.ClientSession() as session:
            # S0: Issue Contract
            async with session.post(f"{self.base_url}/v1/intent/contract", json={
                "issuer": {"agent_id": "derek-node-01"},
                "purpose": "Autonomous Analytical Trajectory"
            }) as resp:
                data = await resp.json()
                self.contract_id = data["result"]["contract_id"]
                print(f"[Derek] Contract secured: {self.contract_id}")

            # S0 -> S1: Data Selection
            res1 = await self._step(session, "select_data", "100 * 2")
            print(f"[Derek] S1 Selection Result: {res1}")

            # S1 -> S2: Analysis
            res2 = await self._step(session, "execute_analysis", "200 / 4")
            print(f"[Derek] S2 Analysis Result: {res2}")

            # S2 -> S3: Reporting
            res3 = await self._step(session, "finalize_reporting", "50 + 25")
            print(f"[Derek] S3 Reporting Result: {res3}")

            # S3 -> S4: Termination
            res4 = await self._step(session, "terminate", "75")
            print(f"[Derek] S4 Termination Result: {res4}")

    async def _step(self, session, transition, payload):
        async with session.post(f"{self.base_url}/v1/tool/execute", json={
            "contract_id": self.contract_id,
            "transition": transition,
            "code_payload": payload
        }) as resp:
            return await resp.json()

if __name__ == "__main__":
    asyncio.run(DerekSovereignAgent().execute_trajectory())
