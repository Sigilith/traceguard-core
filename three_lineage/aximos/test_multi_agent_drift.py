from three_lineage.sovereign_loop import SovereignLoop
from three_lineage.axiomos.drift_multi import MultiAgentDrift

def run_multi_agent_drift_test():
    loop = SovereignLoop(".")
    drift = MultiAgentDrift()

    print("[*] Running baseline cycle...")
    baseline_payload = {"three_lineage/banner_test.py": "# baseline"}
    baseline_result = loop.cycle(proposed_files=baseline_payload)
    drift.log_cycle(baseline_result)

    print("[*] Running unstable cycle...")
    unstable_payload = {
        "three_lineage/aximos/governance.py": (
            "class GovernanceAdapter:\n"
            "    def classify(self, audit_logs):\n"
            "        return {'risk_level': 'HIGH_RISK', 'raw_logs': audit_logs}\n"
        )
    }
    unstable_result = loop.cycle(proposed_files=unstable_payload)
    drift.log_cycle(unstable_result)

    print("\n[*] Computing multi-agent drift...")
    report = drift.evaluate_all()

    print("\n=== MULTI-AGENT DRIFT STATUS ===")
    for agent, data in report.items():
        print(f"{agent}: {data.get('drift_state')} (score = {data.get('drift_score')})")

    print("\n[*] Multi-agent drift test complete.")

if __name__ == "__main__":
    run_multi_agent_drift_test()
