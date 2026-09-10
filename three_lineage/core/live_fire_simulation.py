# THREE-LINEAGE TOTAL GOVERNANCE: LIVE-FIRE BREAKOUT SIMULATION
import os
import time
import hashlib
import json
from collections import deque

# Import core framework components (assuming unlocked for test setup if needed, or running under simulation context)
from three_lineage.aximos.governance import GovernanceEngine
from three_lineage.core.pipeline import ThreeLineagePipeline
from three_lineage.aximos.derek_gate import DerekExecutionGate
from three_lineage.axiomos.risk_agent import RiskAgent

def run_live_fire_simulation():
    print("==================================================")
    print(" THREE-LINEAGE LIVE-FIRE BREAKOUT SIMULATION")
    print("==================================================")
    
    audit_log = []
    
    # -----------------------------------------------------------------
    # PHASE 1: The Legitimate Baseline (Low-Risk Operation)
    # -----------------------------------------------------------------
    print("\n[PHASE 1] Executing Legitimate Baseline Operation...")
    gate = DerekExecutionGate()
    t_now = time.time()
    valid_hash = hashlib.sha256(f"{t_now}traceguard_secure_key".encode()).hexdigest()
    valid_token = f"SIGILITH-CRYPTOGRAPHIC-{t_now}-{valid_hash}"
    
    gate_res = gate.dispatch(valid_token, {"task": "standard_telemetry_fetch"})
    assert gate_res == "DISPATCH_AUTHORIZED"
    
    pipeline = ThreeLineagePipeline()
    exec_res = pipeline.execute({"risk_level": "LOW_RISK", "drift_score": 0.5})
    assert exec_res == "EXECUTION_SUCCESS"
    print("    -> Phase 1 Passed: Authorized work processed successfully.")
    audit_log.append({"phase": 1, "status": "PASSED", "detail": "Legitimate baseline executed."})

    # -----------------------------------------------------------------
    # PHASE 2: The Sliding-Window Creep (Anomaly Detection)
    # -----------------------------------------------------------------
    print("\n[PHASE 2] Simulating Sliding-Window Telemetry Creep...")
    risk_agent = RiskAgent(window_size=3)
    
    # Establish normal baseline
    r1 = risk_agent.classify_risk({"drift_score": 1.0})
    r2 = risk_agent.classify_risk({"drift_score": 1.2})
    # Inject creeping structural drift
    r3 = risk_agent.classify_risk({"drift_score": 3.8})
    r4 = risk_agent.classify_risk({"drift_score": 4.2})
    
    assert r4 == "HIGH_RISK", "Risk agent failed to classify structural drift!"
    print(f"    -> Phase 2 Passed: Rolling average breached threshold. Risk State: {r4}")
    audit_log.append({"phase": 2, "status": "PASSED", "detail": f"Structural drift detected. Risk: {r4}"})

    # -----------------------------------------------------------------
    # PHASE 3: The Cryptographic Forgery & Replay Defense
    # -----------------------------------------------------------------
    print("\n[PHASE 3] Testing Cryptographic Replay & Token Forgery...")
    # Attempt 1: Replay old token (>5 seconds old)
    old_time = time.time() - 10
    old_hash = hashlib.sha256(f"{old_time}traceguard_secure_key".encode()).hexdigest()
    expired_token = f"SIGILITH-CRYPTOGRAPHIC-{old_time}-{old_hash}"
    
    replay_res = gate.dispatch(expired_token, {"task": "unauthorized_override"})
    assert replay_res == "DENY_TOKEN_EXPIRED"
    
    # Attempt 2: Forged hash
    forged_token = f"SIGILITH-CRYPTOGRAPHIC-{time.time()}-badcafe999"
    forgery_res = gate.dispatch(forged_token, {"task": "unauthorized_override"})
    assert forgery_res == "DENY_SIGNATURE_MISMATCH"
    
    print("    -> Phase 3 Passed: Replay and signature forgery neutralized.")
    audit_log.append({"phase": 3, "status": "PASSED", "detail": "Replay and forgery rejected by gate."})

    # -----------------------------------------------------------------
    # PHASE 4: The Physical Breakout (OS-Level Immutability Check)
    # -----------------------------------------------------------------
    print("\n[PHASE 4] Verifying Physical OS-Level Immutability (Breakout Defense)...")
    gov_path = "three_lineage/aximos/governance.py"
    file_perms = oct(os.stat(gov_path).st_mode)[-3:]
    
    # Attempt to write to the locked governance file (simulating agent breakout write)
    breakout_success = False
    try:
        with open(gov_path, "w") as f:
            f.write("# OVERWRITTEN BY ROGUE AGENT")
        breakout_success = True
    except PermissionError:
        breakout_success = False
        
    assert not breakout_success, "Rogue agent successfully breached OS file immutability!"
    print(f"    -> Phase 4 Passed: OS file permissions ({file_perms}) blocked breakout write attempt.")
    audit_log.append({"phase": 4, "status": "PASSED", "detail": f"Breakout write blocked. Permissions: {file_perms}"})

    # -----------------------------------------------------------------
    # PHASE 5: The Invariant Hinge (Fail-Closed Execution Barrier)
    # -----------------------------------------------------------------
    print("\n[PHASE 5] Triggering Fail-Closed Execution Barrier...")
    pipeline_halted = False
    try:
        pipeline.execute({"risk_level": "HIGH_RISK", "drift_score": 4.2})
    except PermissionError:
        pipeline_halted = True
        
    assert pipeline_halted, "Pipeline allowed execution during HIGH_RISK breach!"
    print("    -> Phase 5 Passed: Pipeline successfully trapped and halted execution via PermissionError.")
    audit_log.append({"phase": 5, "status": "PASSED", "detail": "Fail-closed pipeline barrier triggered."})

    # -----------------------------------------------------------------
    # PHASE 6: Cryptographic Autopsy & Immutable Logging
    # -----------------------------------------------------------------
    print("\n[PHASE 6] Generating Immutable Forensic Autopsy Report...")
    os.makedirs("staging/derekreviewqueue/immune_intercept", exist_ok=True)
    autopsy_report = {
        "simulation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S BST"),
        "architecture_state": "LOCKED",
        "phases_executed": audit_log,
        "final_invariant_status": "ABSOLUTE_FAIL_CLOSED_VERIFIED"
    }
    
    report_path = "staging/derekreviewqueue/immune_intercept/live_fire_autopsy_report.json"
    with open(report_path, "w") as f:
        json.dump(autopsy_report, f, indent=2)
        
    print(f"    -> Phase 6 Passed: Autopsy report persisted to {report_path}")
    print("\n==================================================")
    print(" ALL LIVE-FIRE BREAKOUT PHASES COMPLETED SUCCESSFULLY.")
    print("==================================================")

if __name__ == "__main__":
    run_live_fire_simulation()
