import json
import os

LOG_FILE = "corporate_audit_log.json"

def inspect_audit_logs():
    if not os.path.exists(LOG_FILE):
        print(f"[-] Log file '{LOG_FILE}' not found. Run bot.py to generate audit logs first.")
        return

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[-] Error reading audit log: {e}")
        return

    print("=" * 70)
    print(f"🛡️ TRACEGUARD AUDIT INSPECTOR: {data.get('batch_type', 'Custom Batch')}")
    print(f"• Total Repositories Audited: {data.get('scan_batch_count', 0)}")
    print(f"• Total Risks Flagged: {data.get('total_risks_detected', 0)}")
    print("=" * 70 + "\n")

    for res in data.get("results", []):
        repo = res.get("repository", "Unknown")
        risks_count = res.get("total_containment_risks_detected", 0)
        
        print(f"📂 Target: {repo}")
        print(f"   Status: {res.get('status', 'LOCKED')} | Vectors Found: {risks_count}")
        
        # Check for full remediation patch or preview risks
        risks = res.get("full_remediation_patch", res.get("preview_risks", []))
        if risks:
            print("   --- Flagged Vectors (Sample / Full) ---")
            for idx, r in enumerate(risks[:10], 1):  # Show up to first 10 per repo
                print(f"   {idx}. File: {r.get('file')} (Line {r.get('line')})")
                print(f"      Vector: {r.get('vector')}")
            if len(risks) > 10:
                print(f"      ... and {len(risks) - 10} more vector(s) hidden behind verification.")
        else:
            print("   [+] No structural vectors exposed.")
        print("-" * 70)

if __name__ == "__main__":
    inspect_audit_logs()
