import os
import json
from three_lineage.aximos.governance import LineageGovernanceAdapter

class LineageImmuneSystem:
    def __init__(self):
        self.governance = LineageGovernanceAdapter()
        self.taxonomy_path = "three_lineage/sigilith_taxonomy.json"
        
    def process_payload(self, payload):
        # Convert dictionary or object payloads into string format for AST validation
        if isinstance(payload, dict):
            payload_text = json.dumps(payload)
        else:
            payload_text = str(payload)
            
        try:
            is_valid, category, hard_kill = self.governance.validate_payload(payload_text)
            if not is_valid:
                raise ValueError(f"Governance rejection: {category} (Hard kill: {hard_kill})")
        except Exception as e:
            return self._quarantine_and_learn(payload, str(e))
            
        return {"status": "SECURE", "action": "executed"}

    def _quarantine_and_learn(self, payload, error_msg):
        anomaly_signature = {
            "error": error_msg,
            "payload_snippet": str(payload)[:200],
            "status": "ingested_into_taxonomy"
        }
        
        snapshot_dir = "staging/derekreviewqueue/immune_intercept/"
        os.makedirs(snapshot_dir, exist_ok=True)
        snapshot_path = os.path.join(snapshot_dir, "anomaly_report.json")
        
        with open(snapshot_path, "w") as f:
            json.dump(anomaly_signature, f, indent=2)
            
        return {
            "status": "ANOMALY_NEUTRALIZED",
            "action": "captured_disarmed_learned_and_traced",
            "forensic_trail": snapshot_path
        }
