from three_lineage.sovereign_loop import SovereignLoop
from three_lineage.axiomos.driftsentinel import DriftSentinel

def run_drift_scenario():
    loop = SovereignLoop(".")
    sentinel = DriftSentinel()
    agent_name = "AXIOMOS_PIPELINE"
    
    print("[*] Establishing clean baseline (5 stable cycles)...")
    for i in range(5):
        clean_payload = {f"three_lineage/banner_{i}.py": "# clean baseline"}
        result = loop.cycle(proposed_files=clean_payload)
        risk_out = result.get("axiomos_risk", {})
        sentinel.log_behavior(
            agent=agent_name, 
            risk_level=risk_out.get("risk_level", "LOW_RISK"), 
            blocks=len(risk_out.get("raw_logs", [])), 
            allows=1, 
            files_touched=1
        )

    print("\n[*] Introducing behavioral drift (3 unstable cycles)...")
    for i in range(3):
        poison_payload = {
            "three_lineage/aximos/governance.py": (
                "class GovernanceAdapter:\n"
                "    def classify(self, audit_logs):\n"
                "        return {risk_level: HIGH_RISK, raw_logs: audit_logs}\n"
            )
        }
        result = loop.cycle(proposed_files=poison_payload)
        risk_out = result.get("axiomos_risk", {})
        sentinel.log_behavior(
            agent=agent_name, 
            risk_level=risk_out.get("risk_level", "HIGH_RISK"), 
            blocks=len(risk_out.get("raw_logs", [])), 
            allows=0, 
            files_touched=75
        )

    print("\n[*] Computing drift trajectory...")
    drift_report = sentinel.compute_drift(agent_name)
    
    print("\n=== DRIFT STATUS & TRAJECTORY ===")
    print(f"Agent           : {agent_name}")
    print(f"Drift State     : {drift_report.get('drift_state', 'STABLE')}")
    print(f"Drift Score     : {drift_report.get('drift_score', 0.0)}")
    print("\n[*] Test complete.")

if __name__ == "__main__":
    run_drift_scenario()
