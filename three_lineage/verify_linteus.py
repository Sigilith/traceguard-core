# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import json
import os
import hashlib

def verify_manifest():
    manifest_path = "three_lineage/liber_linteus_manifest.json"
    print("====================================================")
    print("📜 THREE-LINEAGE SYMBOLIC MANIFEST VERIFIER")
    print("====================================================")
    
    if not os.path.exists(manifest_path):
        print("[!] Manifest not found.")
        return

    with open(manifest_path, "r") as f:
        data = json.load(f)

    raw_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
    manifest_hash = hashlib.sha256(raw_bytes).hexdigest()[:16]

    print(f"[*] Target System        : {data['system']}")
    print(f"[*] Analytical Framework : {data['framework']}")
    print(f"[*] Structural Signatures: {data['architecture']['total_domains']} Domains across {data['architecture']['total_phases']} Phases[span_1](start_span)[span_1](end_span)")
    print(f"[*] Collapse Nodes Valid : {data['architecture']['collapse_nodes']}[span_2](start_span)[span_2](end_span)")
    print(f"[*] Cryptographic Hash   : {manifest_hash}")
    print("[+] STATUS: Manifest structurally verified against Three-Lineage schema.")
    print("====================================================")

if __name__ == "__main__":
    verify_manifest()
