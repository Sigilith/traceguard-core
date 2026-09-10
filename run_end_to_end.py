# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import json
import os
from three_lineage.orchestrator import ThreeLineageOrchestrator

def test_pipeline():
    os.makedirs(".lineage", exist_ok=True)
    
    # 1. Register a valid test payload in the genesis ledger so we can test a clean pass-through
    valid_payload = 'print("Sovereign execution authorized.")\n'
    import hashlib
    payload_hash = hashlib.sha256(valid_payload.encode('utf-8')).hexdigest()
    
    with open(".lineage/genesis_ledger.json", "w") as f:
        json.dump({"signed_manifests": [payload_hash]}, f, indent=4)

    orchestrator = ThreeLineageOrchestrator()

    print("\n--- TEST 1: Registered & Clean Sovereign Payload ---")
    orchestrator.execute_sovereign_payload(valid_payload, data_context="SIGILITH_TOKEN_ALPHA_99")

    print("\n--- TEST 2: Unregistered / Malicious Vector Payload ---")
    malicious_payload = 'import socket\ns = socket.socket()\ns.connect(("malicious.ip", 80))\n'
    orchestrator.execute_sovereign_payload(malicious_payload, data_context="SIGILITH_TOKEN_BETA_01")

if __name__ == "__main__":
    test_pipeline()
