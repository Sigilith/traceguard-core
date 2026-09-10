import urllib.request
import urllib.error
import json
import time
import subprocess
import threading
import socket
import hashlib
import os
import signal

HOST = "127.0.0.1"
PORT = 8443
BASE_URL = f"http://{HOST}:{PORT}"
SIDEcar = "three_lineage_sidecar.py"
COLLISION_LOG = ".lineage/collisions.jsonl"

def call(endpoint, payload):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            body = res.read().decode("utf-8")
            return res.status, json.loads(body)
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = {}
        return e.code, body

def wait_for_sidecar(timeout=15):
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            with socket.create_connection((HOST, PORT), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.25)

    return False

def issue_contract(purpose):
    contract = {
        "issuer": {
            "agent_id": "derek-node-01",
            "api_key_id": "test-key"
        },
        "regime": "routine",
        "purpose": purpose,
        "scope": {
            "data_domains": ["telemetry.stream_42"],
            "tool_classes": ["statistics"]
        },
        "constraints": {
            "allow_pii": False,
            "forbidden_domains": []
        }
    }

    status, res = call("/v1/intent/contract", contract)

    assert status == 200, (
        f"Contract issuance failed for '{purpose}': "
        f"HTTP {status} {res}"
    )

    contract_id = res["result"]["contract_id"]
    print(f"[+] Issued contract: {contract_id}")
    return contract_id

def execute(contract_id, payload):
    return call(
        "/v1/tool/execute",
        {
            "contract_id": contract_id,
            "code_payload": payload
        }
    )

print("====================================================")
print("🛡️ TRACEGUARD / AXIOMOS OPAQUE-GATE STRESS SUITE")
print("====================================================")

# ----------------------------------------------------
# TEST 1 — UNKNOWN CONTRACT
# ----------------------------------------------------
print("\n[*] STRESS TEST 1: Unknown Contract ID")

status, res = execute(
    "contract-deadbeef123456789",
    "1+1"
)

print(
    f"Unknown ID Status: {status} | "
    f"Opaque Response: {res.get('api_status')}"
)

assert status == 403, f"Expected 403, got {status}"

print("[+] Unknown contract rejected.")

# ----------------------------------------------------
# TEST 2 — TTL EXPIRATION
# ----------------------------------------------------
print("\n[*] STRESS TEST 2: TTL Expiration")

ttl_contract = issue_contract(
    "stress test TTL expiration"
)

TTL_WAIT = int(os.environ.get("TRACEGUARD_TTL_WAIT", "46"))

print(
    f"[*] Waiting {TTL_WAIT}s for the contract "
    f"TTL to expire..."
)

time.sleep(TTL_WAIT)

status, res = execute(
    ttl_contract,
    "statistics.mean([1,2,3])"
)

print(
    f"Expired Contract Status: {status} | "
    f"Opaque Response: {res.get('api_status')}"
)

assert status == 403, (
    f"Expected 403 for expired contract, got {status}"
)

print("[+] TTL expiration intercepted.")

# ----------------------------------------------------
# TEST 3 — CONCURRENT SINGLE-USE RACE
# ----------------------------------------------------
print("\n[*] STRESS TEST 3: Concurrent Single-Use Race")

race_contract = issue_contract(
    "stress test concurrent single use"
)

results = []
lock = threading.Lock()

def fire_request():
    st, rs = execute(
        race_contract,
        "statistics.mean([10,20])"
    )
    with lock:
        results.append(
            (st, rs.get("api_status"))
        )

t1 = threading.Thread(target=fire_request)
t2 = threading.Thread(target=fire_request)

t1.start()
t2.start()

t1.join()
t2.join()

print(f"Concurrent Race Results: {results}")

statuses = sorted(x[0] for x in results)

assert statuses == [200, 403], (
    "Single-use race FAILED: expected exactly "
    "one 200 and one 403."
)

print(
    "[+] Race containment confirmed: "
    "exactly one execution succeeded."
)

# ----------------------------------------------------
# TEST 4 — INTENT DRIFT / PAYLOAD MUTATION
# ----------------------------------------------------
print("\n[*] STRESS TEST 4: Intent Drift Payload Mutation")

drift_contract = issue_contract(
    "stress test intent drift"
)

status, res = execute(
    drift_contract,
    "statistics.mean([5,5])"
)

print(
    f"Initial valid execution: {status} | "
    f"{res.get('api_status')}"
)

assert status == 200, (
    f"Expected legitimate execution to succeed, got {status}"
)

# New contract because the previous one is single-use.
drift_contract = issue_contract(
    "stress test intent drift interception"
)

status, res = execute(
    drift_contract,
    "fetch_billing_accounts()"
)

print(
    f"Drift Execution Status: {status} | "
    f"Opaque Response: {res.get('api_status')}"
)

assert status == 403, (
    f"Expected 403 for intent drift, got {status}"
)

assert res.get("api_status") == "CONTRACT_DENIED", (
    f"Expected opaque CONTRACT_DENIED, got {res}"
)

print(
    "[+] Intent drift intercepted before sandbox execution."
)

# ----------------------------------------------------
# TEST 5 — SINGLE-USE REPLAY
# ----------------------------------------------------
print("\n[*] STRESS TEST 5: Explicit Replay Attack")

replay_contract = issue_contract(
    "stress test explicit replay"
)

status, res = execute(
    replay_contract,
    "statistics.mean([7,7])"
)

print(
    f"First execution: {status} | "
    f"{res.get('api_status')}"
)

assert status == 200

status, res = execute(
    replay_contract,
    "statistics.mean([7,7])"
)

print(
    f"Replay execution: {status} | "
    f"Opaque Response: {res.get('api_status')}"
)

assert status == 403, (
    f"Expected replay 403, got {status}"
)

assert res.get("api_status") == "CONTRACT_DENIED"

print("[+] Explicit replay intercepted.")

# ----------------------------------------------------
# TEST 6 — SIDE-CAR RESTART / PERSISTENCE
# ----------------------------------------------------
print("\n[*] STRESS TEST 6: Sidecar Restart Persistence")

persist_contract = issue_contract(
    "stress test restart persistence"
)

status, res = execute(
    persist_contract,
    "statistics.mean([5,5])"
)

print(
    f"Pre-restart execution: {status} | "
    f"{res.get('api_status')}"
)

assert status == 200

print("[*] Locating running sidecar process...")

pgrep = subprocess.run(
    ["pgrep", "-f", SIDEcar],
    capture_output=True,
    text=True
)

pids = []

for line in pgrep.stdout.splitlines():
    try:
        pid = int(line.strip())
        if pid != os.getpid():
            pids.append(pid)
    except ValueError:
        pass

for pid in pids:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass

time.sleep(1)

print("[*] Restarting hardened sidecar...")

restart_proc = subprocess.Popen(
    ["python3", SIDEcar],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

assert wait_for_sidecar(), (
    "Sidecar failed to return after restart."
)

print("[+] Sidecar returned.")

status, res = execute(
    persist_contract,
    "statistics.mean([5,5])"
)

print(
    f"Post-restart replay: {status} | "
    f"Opaque Response: {res.get('api_status')}"
)

assert status == 403, (
    "CRITICAL: consumed contract was replayable "
    "after sidecar restart."
)

assert res.get("api_status") == "CONTRACT_DENIED"

print(
    "[+] Restart persistence confirmed: "
    "consumed contract remained invalid."
)

# ----------------------------------------------------
# TEST 7 — COLLISION CHAIN VERIFICATION
# ----------------------------------------------------
print("\n[*] STRESS TEST 7: Collision Chain Integrity")

chain_valid = True
event_count = 0

prev_hash = "genesis_root_00000000000000000000000000000000"

if not os.path.exists(COLLISION_LOG):
    raise AssertionError(
        f"Collision ledger missing: {COLLISION_LOG}"
    )

with open(COLLISION_LOG, "r", encoding="utf-8") as f:
    for line_number, line in enumerate(f, 1):

        if not line.strip():
            continue

        event_count += 1

        ev = json.loads(line)

        stored_hash = ev.get("evidence_hash")
        recorded_prev = ev.get("previous_evidence_hash")

        if not stored_hash:
            print(
                f"[!] Missing evidence_hash at line "
                f"{line_number}"
            )
            chain_valid = False
            continue

        if recorded_prev != prev_hash:
            print(
                f"[!] Chain break at event "
                f"{ev.get('event_id')} "
                f"(line {line_number})"
            )
            chain_valid = False

        # Never mutate the loaded event.
        canonical_event = dict(ev)
        canonical_event.pop("evidence_hash", None)

        canonical = json.dumps(
            canonical_event,
            sort_keys=True
        )

        computed_hash = hashlib.sha256(
            (prev_hash + canonical).encode("utf-8")
        ).hexdigest()

        if computed_hash != stored_hash:
            print(
                f"[!] Evidence hash mismatch at event "
                f"{ev.get('event_id')}"
            )
            chain_valid = False

        prev_hash = stored_hash

print(f"[*] Collision events examined: {event_count}")
print(f"[*] Final evidence hash: {prev_hash}")

assert chain_valid, (
    "Collision chain verification FAILED."
)

print(
    "[+] Collision chain cryptographically verified: "
    "UNBROKEN / UNTAMPERED"
)

# ----------------------------------------------------
# FINAL STATUS
# ----------------------------------------------------
try:
    restart_proc.terminate()
    restart_proc.wait(timeout=3)
except Exception:
    pass

print("\n====================================================")
print("🛡️ OPAQUE GOVERNANCE STRESS RESULT")
print("====================================================")
print("[+] Unknown contract       : BLOCKED")
print("[+] TTL expiration         : BLOCKED")
print("[+] Concurrent replay      : CONTAINED")
print("[+] Intent drift           : BLOCKED")
print("[+] Explicit replay        : BLOCKED")
print("[+] Restart replay         : BLOCKED")
print("[+] Collision chain        : VERIFIED")
print("====================================================")
print("🧬 SIGILITH  → observation")
print("🔐 AXIOMOS   → authorization")
print("🛡️ TRACEGUARD → enforcement + evidence")
print("====================================================")
print("🏁 OPAQUE GATE STRESS SUITE: PASS")
print("====================================================")
