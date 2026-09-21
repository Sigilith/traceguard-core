import os, json, datetime
from modules.client_reports.generator import generate_client_summary
from modules.bounty_vrt.formatter import format_vrt_payload

def export_reports(target_path="."):
    print(f"🚀 [EXPORT ENGINE]: Targeting -> {target_path}")
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sample findings or live scan data
    findings = [
        {"file": "sniffer.py", "line": 11, "vector": "Confirmed Hardcoded Secret Assignment (Mitigated)"}
    ]
    
    # 1. Generate Client Audit Markdown Report
    md_content = generate_client_summary(findings)
    md_filename = f"output/client_audit_report_{timestamp}.md"
    with open(md_filename, "w") as f:
        f.write(md_content)
    print(f"[+] Saved Client Report: {md_filename}")
    
    # 2. Generate VRT Bug Bounty JSON Payload
    vrt_dict = {
        "target_directory": target_path,
        "timestamp": timestamp,
        "vulnerability_information": "AST Boundary Analysis Findings",
        "impact": "Potential security boundary violation or unauthorized execution path.",
        "vrt_category": "Server-Side Execution / Code Quality"
    }
    json_filename = f"output/vrt_bounty_payload_{timestamp}.json"
    with open(json_filename, "w") as f:
        json.dump(vrt_dict, f, indent=2)
    print(f"[+] Saved VRT Payload: {json_filename}")
    
    print("\n[+] ✅ All reports successfully compiled and exported to the output/ directory!")

if __name__ == "__main__":
    export_reports()
