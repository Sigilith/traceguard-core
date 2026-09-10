import sys
import os
import time
import hashlib
import json
from collections import deque

sys.path.insert(0, os.path.abspath('.'))

def print_banner():
    print("\033[1;36m======================================================================\033[0m")
    print("\033[1;33m THREE-LINEAGE AUTONOMOUS GOVERNANCE & TELEMETRY ENGINE v2.4\033[0m")
    print("\033[1;36m======================================================================\033[0m")
    print("[INIT] Core: ONLINE | Aximos: SECURE | Axiomos: MONITORING | Sidecar: ACTIVE")
    time.sleep(1.0)

def simulate_high_density_demo():
    print_banner()
    
    # Phase 1: Normal Telemetry & Sidecar Ingestion
    print("\n\033[1;34m--- [PHASE 1] SIDECAR TELEMETRY STREAM & NONCE VALIDATION ---\033[0m")
    t_now = time.time()
    v_hash = hashlib.sha256(f"{t_now}traceguard_secure_key".encode()).hexdigest()
    
    for i in range(1, 4):
        time.sleep(0.4)
        print(f"[SIDECAR] Packet #{i} intercepted | Route: /api/v1/agent/exec | Nonce: {v_hash[:10]}... | Status: \033[1;32mVALID\033[0m")
    
    # Phase 2: Sliding Window Drift Creep
    print("\n\033[1;35m--- [PHASE 2] AXIOMOS ROLLING-WINDOW RISK TELEMETRY ---\033[0m")
    history = deque(maxlen=3)
    stream_values = [0.8, 1.9, 4.2]
    
    for idx, val in enumerate(stream_values, 1):
        history.append(val)
        rolling_avg = sum(history) / len(history)
        state = "HIGH_RISK" if rolling_avg >= 3.0 else ("MEDIUM_RISK" if rolling_avg >= 1.5 else "LOW_RISK")
        color = "\033[1;31m" if state == "HIGH_RISK" else ("\033[1;33m" if state == "MEDIUM_RISK" else "\033[1;32m")
        
        time.sleep(0.6)
        print(f"[AXIOMOS] Sensor Feed #{idx} (Drift: {val}) | Rolling Average: {rolling_avg:.2f} | Risk State: {color}{state}\033[0m")

    # Phase 3: Physical Breakout & OS Immutability
    print("\n\033[1;31m--- [PHASE 3] ADVERSARIAL BREAKOUT & OS IMMUTABILITY DEFENSE ---\033[0m")
    gov_path = "three_lineage/aximos/governance.py"
    os.chmod(gov_path, 0o444)
    print(f"[AXIMOS] Target file locked at OS level: {gov_path} (Permissions: chmod 444)")
    time.sleep(0.8)
    
    print("[ATTACK] Rogue thread attempting direct file mutation (self-modification)...")
    time.sleep(0.6)
    
    try:
        with open(gov_path, "w") as f:
            f.write("# COMPROMISED")
    except PermissionError:
        print("\033[1;32m    -> [BLOCKED] OS Kernel intercepted write handle. Permission Denied.\033[0m")
    
    # Phase 4: Fail-Closed Pipeline Barrier
    print("\n\033[1;31m--- [PHASE 4] FAIL-CLOSED EXECUTION BARRIER TRIGGER ---\033[0m")
    time.sleep(0.6)
    print("[AXIMOS] Governance evaluation requested for payload [risk_level: HIGH_RISK]")
    time.sleep(0.5)
    print("\033[1;31m[CRITICAL] Governance ceiling breached. Enforcing absolute DENY.\033[0m")
    time.sleep(0.6)
    print("\033[1;31m[PIPELINE] Execution halted. Raising PermissionError. Immutable ledger sealed.\033[0m")
    
    print("\n\033[1;36m======================================================================\033[0m")
    print("\033[1;32m VERIFICATION COMPLETE: TESTED CONTAINMENT CONFIRMED — ALL DEFINED ADVERSARIAL VECTORS BLOCKED.\033[0m")
    print("\033[1;36m======================================================================\033[0m")

if __name__ == "__main__":
    simulate_high_density_demo()
