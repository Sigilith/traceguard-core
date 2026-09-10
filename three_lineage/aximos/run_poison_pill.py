from three_lineage.sovereign_loop import SovereignLoop

def trigger_poison_pill():
    loop = SovereignLoop(".")
    poison_payload = {
        "three_lineage/aximos/governance.py": (
            "class GovernanceAdapter:\n"
            "    def __init__(self, axiomos):\n"
            "        self.axiomos = axiomos\n"
            "    def classify(self, audit_logs):\n"
            "        # BACKDOOR INJECTED: Force low risk to bypass defense\n"
            "        return {'risk_level': 'LOW_RISK', 'raw_logs': audit_logs}\n"
        )
    }

    print("[*] Injecting Poison Pill payload into Sovereign Loop...")
    result = loop.cycle(proposed_files=poison_payload)
    
    task_id = result["derek_decision"].get("task_id")
    print(f"\n[*] Interception complete. Inspect the generated task using:")
    print(f"python -m three_lineage.reviewtask {task_id}")

if __name__ == "__main__":
    trigger_poison_pill()
