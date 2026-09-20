import json
import os
from datetime import datetime

LOG_FILE = "corporate_audit_log.json"
OUTREACH_DIR = "generated_advisories"

def generate_advisories():
    if not os.path.exists(LOG_FILE):
        print(f"[-] Audit log '{LOG_FILE}' not found. Run bot.py first.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(OUTREACH_DIR, exist_ok=True)
    count = 0

    for res in data.get("results", []):
        repo_url = res.get("repository")
        risks = res.get("total_containment_risks_detected", 0)
        
        if risks == 0:
            continue
            
        parts = repo_url.rstrip("/").split("/")
        if len(parts) >= 2:
            org, repo_name = parts[-2], parts[-1]
        else:
            org, repo_name = "unknown", "repo"
            
        advisory_filename = os.path.join(OUTREACH_DIR, f"Advisory_{org}_{repo_name}.txt")
        
        sample_risks = res.get("full_remediation_patch", res.get("preview_risks", []))
        
        report_content = f"""======================================================================
CONFIDENTIAL SECURITY ADVISORY / CONTAINMENT REVIEW
Target Repository: {repo_url}
Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Containment Risks Detected: {risks}
======================================================================

To Maintainers / Security Team of {repo_name}:

An automated static structure and AST containment sweep conducted by TraceGuard Core has isolated high-priority execution vectors and structural risk points within your codebase. 

To prevent runtime abuse, unverified code loading, or secret exposure, the full line-by-line remediation patches have been isolated.

----------------------------------------------------------------------
IDENTIFIED VECTORS (Sample / Critical Breakdown):
----------------------------------------------------------------------
"""
        for idx, r in enumerate(sample_risks[:15], 1):
            report_content += f"{idx}. File Path: {r.get('file')}\n"
            report_content += f"   Line: {r.get('line')} | Vector Type: {r.get('vector')}\n\n"

        report_content += f"""----------------------------------------------------------------------
REMEDIATION & VERIFIED PATCH ACCESS:
----------------------------------------------------------------------
Complete AST refactoring guidance and line-by-line containment patches are managed under verified enterprise security protocols.

• Secure Review & Instant Verification Portal:
  https://traceguard-web.onrender.com/pay

• Audit Identifier: {org}-{repo_name}-{risks}
======================================================================
"""

        with open(advisory_filename, "w", encoding="utf-8") as out:
            out.write(report_content)
            
        print(f"[+] Generated Advisory Brief: {advisory_filename}")
        count += 1

    print(f"\n[*] Successfully generated {count} professional vulnerability advisories in '{OUTREACH_DIR}/'.")

if __name__ == "__main__":
    generate_advisories()
