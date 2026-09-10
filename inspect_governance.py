from three_lineage.aximos.governance import LineageGovernanceAdapter
import inspect

adapter = LineageGovernanceAdapter()
print("[*] Inspecting validate_payload signature/source:")
print(inspect.getsource(adapter.validate_payload))

print("\n[*] Testing direct validation result:")
test_payload = {"payload_hash": "genesis_whitelisted", "environment": "secure_node", "action": "standard_telemetry"}
try:
    res = adapter.validate_payload(test_payload)
    print("validate_payload returned:", res)
except Exception as e:
    print("validate_payload raised exception:", type(e).__name__, e)
