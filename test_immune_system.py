from three_lineage.immune_orchestrator import LineageImmuneSystem

immune = LineageImmuneSystem()

print("[*] Testing Immune System with Malicious Anomaly Payload...")
bad_payload = {"mutation": "unauthorized_ast_injection", "risk": "high"}
print("Result:", immune.process_payload(bad_payload))

print("\n[*] Testing Immune System with Whitelisted Governance Payload...")
# Provide structure matching the hardened LineageGovernanceAdapter criteria
good_payload = {
    "payload_hash": "genesis_whitelisted",
    "environment": "secure_node",
    "action": "standard_telemetry"
}
print("Result:", immune.process_payload(good_payload))
