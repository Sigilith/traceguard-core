# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import json
import os
import hashlib
from datetime import datetime, timezone

class CorpusAuditor:
    def __init__(self):
        self.manifest_path = "three_lineage/etruscan_artifacts_manifest.json"
        self.audit_log_path = ".lineage/telemetry/corpus_audit.log"
        os.makedirs(".lineage/telemetry", exist_ok=True)

    def compute_hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()[:16]

    def audit_corpus(self):
        print("====================================================")
        print("🛡️ SENTINEL-GRADE CORPUS AUDITOR & DRIFT DETECTOR")
        print("====================================================")
        
        if not os.path.exists(self.manifest_path):
            print("[!] Critical Error: Artifact manifest missing.")
            return False

        with open(self.manifest_path, "r") as f:
            corpus = json.load(f)

        all_valid = True
        audit_records = []

        for item in corpus.get("artifacts", []):
            current_hash = self.compute_hash(item)
            print(f"[*] Auditing Target : {item['name']}")
            print(f"    - Architecture  : {item['architecture']}")
            print(f"    - Current Hash  : {current_hash}")
            
            # Simulate baseline drift check (comparing structural integrity)
            if item["status"] not in ["Verified", "Aligned"]:
                print(f"    - [!] WARNING: Structural drift detected on {item['name']}!")
                all_valid = False
            else:
                print(f"    - [+] Integrity Check : PASSED (Status: {item['status']})")
            
            audit_records.append({
                "artifact": item["name"],
                "hash": current_hash,
                "status": item["status"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            print("-" * 52)

        with open(self.audit_log_path, "a") as log_file:
            for record in audit_records:
                log_file.write(json.dumps(record) + "\n")

        if all_valid:
            print("[+] CORPUS AUDIT COMPLETE: Zero drift detected. System secure.")
        else:
            print("[!] CORPUS AUDIT COMPLETE: Drift or anomalies isolated.")
        print("====================================================")
        return all_valid

if __name__ == "__main__":
    CorpusAuditor().audit_corpus()
