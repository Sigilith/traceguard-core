import time
import subprocess
import sys
import datetime

def log(msg):
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"[{ts}] {msg}")

def check_health():
    # Run Rust verifier binary to check collision chain integrity
    res = subprocess.run(["cargo", "run", "--manifest-path", "Cargo.toml", "--release", "--quiet"], capture_output=True)
    if res.returncode == 0:
        log("HEALTH OK: Cryptographic collision chain verified untampered.")
    else:
        log("CRITICAL FAULT: Ledger integrity failure detected!")
        sys.exit(1)

if __name__ == "__main__":
    log("Starting TraceGuard Beacon & Integrity Monitor...")
    try:
        while True:
            check_health()
            time.sleep(30)
    except KeyboardInterrupt:
        log("Monitor stopped by operator.")
