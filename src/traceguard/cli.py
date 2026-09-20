#!/usr/bin/env python3

import sys
from traceguard.traceguard import TraceGuard
from traceguard.aximos import AXIOMOSEvaluator
from traceguard.evidence import EvidenceLedger
from traceguard.compliance_report import ComplianceReportGenerator
from traceguard.pdf_generator import generate_compliance_pdf

def print_help():
    print("TRACEGUARD CLI // Autonomous Agent Governance SDK")
    print("\nUsage:")
    print("  traceguard <command> [options]")
    print("\nAvailable Commands:")
    print("  demo      Run the full interactive zero-trust pipeline demo")
    print("  verify    Perform independent cryptographic ledger verification")
    print("  audit     Execute a live policy check and generate audit metadata")
    print("  drift     Analyze operational log files for behavioral risk drift")
    print("  pdf       Compile and export the enterprise compliance PDF artifact")
    print("  --help    Show this command reference guide")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "demo":
        run_demo()
    elif command == "verify":
        run_verification()
    elif command == "audit":
        run_audit()
    elif command == "drift":
        run_drift()
    elif command == "pdf":
        run_pdf()
    else:
        print(f"Unknown command: '{command}'. Run 'traceguard --help' for available commands.")
        sys.exit(1)

def run_demo():
    print("=== TRACEGUARD ZERO-TRUST DEMO ===")
    tg = TraceGuard(allowed_actions=["read_logs", "safe_query"])
    ledger = EvidenceLedger()

    res1 = tg.evaluate_action("read_logs")
    ledger.append_entry({"action": "read_logs", "decision": res1})
    print(f"[1] Legitimate action       {res1}")

    res2 = tg.evaluate_action("delete_system_root")
    ledger.append_entry({"action": "delete_system_root", "decision": res2})
    print(f"[2] Unauthorized action     {res2}")

    print(f"[3] Evidence recorded      ✓ (Ledger Index: {len(ledger.chain)-1})")

    is_valid = ledger.verify_integrity()
    print(f"[4] Hash chain verified     {'✓' if is_valid else '✗'}")

    ledger.tamper_with_entry(0, {"action": "tampered", "decision": "BYPASS"})
    tamper_detected = not ledger.verify_integrity()
    print(f"[5] Tamper attempt          {'DETECTED' if tamper_detected else 'MISSED'}")

    ax = AXIOMOSEvaluator(block_threshold=1)
    risk = ax.evaluate_logs(tg.get_logs())
    print(f"[6] AXIOMOS assessment      {risk}")
    print("\nAUDIT STATUS: VERIFIED" if is_valid else "AUDIT STATUS: COMPROMISED")

def run_verification():
    print("=== TRACEGUARD INDEPENDENT EVIDENCE VERIFICATION ===")
    ledger = EvidenceLedger()
    ledger.append_entry({"action": "safe_query", "decision": "ALLOW"})
    ledger.append_entry({"action": "unauthorized", "decision": "BLOCK"})

    integrity = ledger.verify_integrity()
    print(f"Chain Length: {len(ledger.chain)}")
    print(f"Cryptographic Integrity Check: {'PASSED ✓' if integrity else 'FAILED ✗'}")
    print(f"Current Head Hash: {ledger.chain[-1]['current_hash'][:16]}...")

def run_audit():
    print("=== TRACEGUARD COMPLIANCE AUDIT PACKET ===")
    reporter = ComplianceReportGenerator()
    packet = reporter.generate_packet(consequence=3, autonomy=3, oversight=False, violations_detected=1)
    print(packet["risk_classification"])

def run_drift():
    print("=== AXIOMOS BEHAVIORAL DRIFT ANALYSIS ===")
    ax = AXIOMOS(block_threshold=2)
    sample_logs = [
        {"action": "read_data", "decision": "ALLOW"},
        {"action": "unauthorized_drop", "decision": "BLOCK"},
        {"action": "unauthorized_modify", "decision": "BLOCK"}
    ]
    risk = ax.evaluate_logs(sample_logs)
    print(f"Evaluated Log Entries: {len(sample_logs)}")
    print(f"Behavioral Risk Status: {risk}")

def run_pdf():
    print("=== ENTERPRISE PDF EXPORT ===")
    reporter = ComplianceReportGenerator()
    packet = reporter.generate_packet(consequence=3, autonomy=3, oversight=False, violations_detected=1)
    filename = generate_compliance_pdf(packet, "traceguard_compliance_audit.pdf")
    print(f"PDF successfully compiled and saved to '{filename}'.")

if __name__ == "__main__":
    main()
