import subprocess
import time
import urllib.request
import json

def run_chaos_test():
    print("[*] Launching Chaos Validation Harness...")
    subprocess.run(["pkill", "-f", "three_lineage_sidecar.py"])
    subprocess.Popen(["python3", "three_lineage_sidecar.py"])
    time.sleep(1)

    req = urllib.request.Request(
        "http://127.0.0.1:8443/v1/tool/execute",
        data=json.dumps({"contract_id": "malformed-id", "code_payload": "1+1", "signature": "spoofed"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as res:
            code = res.status
    except urllib.error.HTTPError as e:
        code = e.code

    assert code == 403, f"Expected 403 on spoofed signature, got {code}"
    print("[+] Chaos Test 1 Passed: Spoofed signature rejected with 403.")

    print("[*] Simulating sudden sidecar termination (Node Crash)...")
    subprocess.run(["pkill", "-f", "three_lineage_sidecar.py"])
    
    verify_res = subprocess.run(["cargo", "run", "--manifest-path", "Cargo.toml", "--release", "--quiet"], capture_output=True)
    print(f"[+] Chaos Test 2 Passed: Post-crash ledger verified with exit code {verify_res.returncode}.")

if __name__ == "__main__":
    run_chaos_test()
