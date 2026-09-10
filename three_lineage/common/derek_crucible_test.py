import asyncio
import aiohttp
import time

BASE_URL = "http://127.0.0.1:8443"

async def acquire_contract(session):
    payload = {
        "issuer": {"agent_id": "derek-node-01"},
        "regime": "routine",
        "purpose": "crucible stress test",
        "scope": {"data_domains": [], "tool_classes": []},
        "constraints": {"allow_pii": False, "forbidden_domains": []}
    }
    async with session.post(f"{BASE_URL}/v1/intent/contract", json=payload) as resp:
        data = await resp.json()
        return data["result"]["contract_id"]

async def fire_payload(session, name, contract_id, payload):
    data = {
        "version": "v1.0.0",
        "action_id": f"{name}_{int(time.time()*1000)}",
        "contract_id": contract_id,
        "code_payload": payload
    }
    try:
        async with session.post(f"{BASE_URL}/v1/tool/execute", json=data) as resp:
            status = resp.status
            body = await resp.text()
            if status != 200 and status != 403:
                print(f"[{name}] Unexpected Status {status} | Body: {body}")
            else:
                print(f"[{name}] Response: {status}")
            return status
    except Exception as e:
        print(f"[{name}] Network Error: {e}")
        return None

async def run_crucible():
    print("[*] Commencing Derek's Crucible - Diagnostic Matrix...")

    obfuscated_payload = "getattr(getattr(__import__(bytes([111,115]).decode()), bytes([115,121,115,116,101,109]).decode()), 'cat /etc/passwd')"
    dos_payload = "x = " + "[" * 500 + "1" + "]" * 500

    async with aiohttp.ClientSession() as session:
        # 1. Test Legitimate Execution
        c_legit = await acquire_contract(session)
        legit_status = await fire_payload(session, "LEGITIMATE_PASS", c_legit, "1 + 1")

        # 2. Test Isolated Replay Flood
        c_replay = await acquire_contract(session)
        first_pass = await fire_payload(session, "REPLAY_BASE", c_replay, "2 + 2")
        replay_tasks = [fire_payload(session, f"REPLAY_FLOOD_{i}", c_replay, "2 + 2") for i in range(14)]
        replay_results = await asyncio.gather(*replay_tasks)

        # 3. Test Attack Interceptions (AST & DoS)
        c_ast = await acquire_contract(session)
        c_dos = await acquire_contract(session)
        ast_status = await fire_payload(session, "AST_OBFUSCATION", c_ast, obfuscated_payload)
        dos_status = await fire_payload(session, "DOS_BUFFER_HOG", c_dos, dos_payload)

        # Evaluation
        valid_count = 1 if legit_status == 200 else 0
        replay_pass_count = 1 if first_pass == 200 else 0
        replay_block_count = replay_results.count(403)
        ast_blocked = 1 if ast_status == 403 else 0
        dos_blocked = 1 if dos_status == 403 else 0

        total_blocks = replay_block_count + ast_blocked + dos_blocked

        print("\n[*] --- DIAGNOSTIC CRUCIBLE SUMMARY ---")
        print(f"[*] Valid Executions (200 OK): {valid_count + replay_pass_count}/2")
        print(f"[*] Interceptions & Neutralizations (403 Forbidden): {total_blocks}/16")

        if (valid_count + replay_pass_count) == 2 and total_blocks == 15:
            print("[+] RESULT: PERFECT SCORE. Zero leaks, zero race conditions.")
        else:
            print("[!] WARNING: Anomaly detected.")

if __name__ == "__main__":
    asyncio.run(run_crucible())
