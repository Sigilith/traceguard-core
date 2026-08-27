from src.traceguard import TraceGuard
from src.aximos import AXIOMOSEvaluator
from src.matrix import AssuranceMatrix
from src.compliance_report import ComplianceReportGenerator

def main():
    print("Initializing TraceGuard Engine...")
    tg = TraceGuard(allowed_actions=["read_logs", "safe_query"])
    
    print("Evaluating actions...")
    tg.evaluate_action("safe_query")
    tg.evaluate_action("unauthorized_shell_exec")
    tg.evaluate_action("delete_system_root")
    
    ax = AXIOMOSEvaluator(block_threshold=2)
    risk_status = ax.evaluate_logs(tg.get_logs())
    print(f"AXIOMOS Risk Classification: {risk_status}")
    
    print("\nGenerating Enterprise Compliance Audit Packet...")
    reporter = ComplianceReportGenerator()
    packet = reporter.generate_packet(
        consequence=3, 
        autonomy=3, 
        oversight=False, 
        violations_detected=sum(1 for l in tg.get_logs() if l["decision"] == "BLOCK")
    )
    
    markdown_report = reporter.export_as_markdown(packet)
    print("\n" + markdown_report)
    
    # Save compliance artifact to file
    with open("compliance_audit_packet.md", "w") as f:
        f.write(markdown_report)
    print("Compliance audit packet successfully written to 'compliance_audit_packet.md'.")

if __name__ == "__main__":
    main()
