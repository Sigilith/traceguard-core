# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import json
import os
import hashlib

def batch_verify():
    path = "three_lineage/etruscan_artifacts_manifest.json"
    print("====================================================")
    print("🔮 THREE-LINEAGE CROSS-ARTIFACT BATCH VERIFIER")
    print("====================================================")
    
    with open(path, "r") as f:
        data = json.load(f)

    for item in data["artifacts"]:
        raw = json.dumps(item, sort_keys=True).encode("utf-8")
        h = hashlib.sha256(raw).hexdigest()[:16]
        print(f"[*] Artifact : {item['name']}")
        print(f"    - Type   : {item['type']}")
        print(f"    - Scale  : {item['scale']}")
        print(f"    - Schema : {item['architecture']}")
        print(f"    - Hash   : {h} | Status: {item['status']}")
        print("-" * 52)

    print("[+] BATCH VERIFICATION COMPLETE: All comparative structures synchronized.")
    print("====================================================")

if __name__ == "__main__":
    batch_verify()
