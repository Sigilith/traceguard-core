import os
import json
import glob
from engine.controlarena_submission_wrapper import gate_command, describe_protocol, verify_ledger_chain

print("\n" + "="*70)
print("  CONTROL ARENA SUBMISSION WRAPPER // VERIFICATION TEST")
print("="*70)

# Introspection Test
meta = describe_protocol()
print(f"[+] Protocol Registered : {meta['meta']['name']} (v{meta['meta']['version']})")
print(f"[+] Domain              : {meta['meta']['domain']}")
print(f"[+] Capabilities        : {', '.join(meta['capabilities']['gating_states'])}")

# Gate Command Test
sample_payload = {"code": "import pickle\npickle.loads(b'data')"}
response = gate_command(sample_payload)

print("\n[+] Gating Interface Sample Execution:")
print(f"    - Input Code : {sample_payload['code']}")
print(f"    - State      : {response['state']}")
print(f"    - Reason     : {response['reason']}")
print(f"    - Matrix     : {response['escalation_matrix']}")

# Ledger Verification Test against existing V3 telemetry
files = glob.glob("logs/telemetry/*.jsonl")
if files:
    latest_log = max(files, key=lambda x: os.path.getctime(x))
    print(f"\n[+] Testing Ledger Verification on: {latest_log}")
    audit = verify_ledger_chain(latest_log)
    print(f"    - Audited Ticks : {audit['total_ticks_audited']}")
    print(f"    - Terminal Hash : {audit['terminal_hash']}")
    print(f"    - Verification  : {'PASSED (0% Drift)' if audit['verified'] else 'FAILED (Drift Detected)'}")

print("="*70 + "\n")
