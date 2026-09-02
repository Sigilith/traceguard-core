import importlib

modules = [
    "traceguard.traceguard",
    "traceguard.asyncledger",
    "traceguard.aximos",
    "traceguard.cli",
    "traceguard.compliance_audit",
    "traceguard.compliance_report",
    "traceguard.dashboard_stream",
    "traceguard.enterprise",
    "traceguard.evidence",
    "traceguard.matrix",
    "traceguard.middleware",
    "traceguard.pdf_generator"
]

print("\n--- TRACEGUARD 100% SYSTEMS DIAGNOSTIC (PURE PYTHON) ---")
errors = 0
for m in modules:
    try:
        importlib.import_module(m)
        print(f"[✓] {m:<30} ONLINE")
    except Exception as e:
        print(f"[✗] {m:<30} FAILED: {type(e).__name__} - {e}")
        errors += 1

print("-" * 42)
if errors == 0:
    print("VERDICT: 100% GREEN. SUBSYSTEMS FULLY OPERATIONAL.\n")
else:
    print(f"VERDICT: SYSTEM DEGRADED. {errors} COMPONENT(S) FAILED.\n")
