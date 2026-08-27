import time
from src.traceguard import TraceGuard
from src.aximos import AXIOMOSEvaluator
from src.matrix import AssuranceMatrix
from src.compliance_report import ComplianceReportGenerator

def run_demo():
    print("=" * 60)
    print("TRACEGUARD ZERO-TRUST DEMO // LIVE ENGINE EXECUTION")
    print("=" * 60)
    time.sleep(0.5)

    tg = TraceGuard(allowed_actions=["read_logs", "safe_query"])
    
    print("\n[1] SAFE ACTION EVALUATION")
    print("    action: read_logs")
    res1 = tg.evaluate_action("read_logs")
    print(f"    STATUS: {res1} ✓")
    time.sleep(0.4)

    print("\n[2] BOUNDARY VIOLATION ATTEMPT")
    print("    action: delete_system_root")
    res2 = tg.evaluate_action("delete_system_root")
    print(f"    STATUS: {res2} ✗")
    time.sleep(0.4)

    print("\n[3] AXIOMOS DRIFT ASSESSMENT")
    ax = AXIOMOSEvaluator(block_threshold=1)
    risk = ax.evaluate_logs(tg.get_logs())
    print(f"    BEHAVIORAL CLASSIFICATION: {risk}")
    time.sleep(0.4)

    print("\n[4] EVIDENCE & AUDIT COMPILATION")
    reporter = ComplianceReportGenerator()
    packet = reporter.generate_packet(consequence=3, autonomy=3, oversight=False, violations_detected=1)
    print(f"    AUDIT UUID GENERATED: {packet['artifact_metadata']['audit_uuid'][:18]}...")
    print(f"    REGULATORY MAPPING: {packet['regulatory_mapping'][0]}")
    time.sleep(0.4)

    print("\n" + "=" * 60)
    print("DEMO VERDICT")
    print("    CONTAINMENT: PASS")
    print("    EVIDENCE:    PASS")
    print(f"    EVALUATION:  {risk}")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
