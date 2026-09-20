import urllib.request
import urllib.parse
import json
import os
import sys
from datetime import datetime

LEDGER_FILE = "audit_ledger.json"

def load_ledger():
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_ledger(ledger):
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=4)

def fetch_corporate_targets():
    return [
        # Enterprise Cloud & Payments
        "https://github.com/aws/aws-cli",
        "https://github.com/boto/boto3",
        "https://github.com/stripe/stripe-python",
        "https://github.com/twilio/twilio-python",
        "https://github.com/sendgrid/sendgrid-python",
        "https://github.com/DataDog/dd-trace-py",
        "https://github.com/slackapi/python-slack-sdk",
        "https://github.com/celery/celery",
        # Web3 & Blockchain Python Ecosystem
        "https://github.com/ethereum/py-evm",
        "https://github.com/web3/web3.py",
        "https://github.com/ConsenSys/truffle",
        # Core Web & API Frameworks
        "https://github.com/pallets/flask",
        "https://github.com/django/django",
        "https://github.com/psf/requests"
    ]

def log_b2b_lead(result):
    repo_url = result.get("repository")
    risks = result.get("total_containment_risks_detected", 0)
    
    if risks == 0:
        return
        
    lead_message = (
        f"🚨 TraceGuard B2B Enterprise Lead Generated\n"
        f"• Target: {repo_url}\n"
        f"• Risk Vectors Flagged: {risks}\n"
        f"• Action: Audit report locked behind verification.\n"
        f"• Stripe Checkout: https://traceguard-web.onrender.com/pay"
    )
    
    print("\n" + "═" * 70)
    print(f"[!] 💼 B2B LEAD CAPTURED & LOCKED: {repo_url}")
    print(lead_message)
    print("═" * 70 + "\n")

def run_traceguard_scan(repo_url):
    form_data = {'github_url': repo_url}
    data = urllib.parse.urlencode(form_data).encode('utf-8')
    req = urllib.request.Request("https://traceguard-web.onrender.com/scan-git", data=data)
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode())
            risks_found = result.get('total_containment_risks_detected', 0)
            print(f"[+] Scanned Target Repo: {repo_url} | Risks Found: {risks_found}")
            
            if risks_found > 0:
                log_b2b_lead(result)
            return result
    except Exception as e:
        print(f"[-] Scan error for {repo_url}: {e}")
        return None

if __name__ == "__main__":
    ledger = load_ledger()
    target_repos = fetch_corporate_targets()
    
    # Filter out any repository that has already been successfully audited and logged
    pending_repos = []
    for repo in target_repos:
        if repo in ledger and ledger[repo].get("status") == "COMPLETED":
            print(f"[*] Skipping already processed target: {repo}")
        else:
            pending_repos.append(repo)
    
    if not pending_repos:
        print("\n[*] All targets already fully audited and recorded in the ledger. Zero duplicates will be processed.")
        sys.exit(0)
        
    print(f"\n[*] Starting stateful sweep across {len(pending_repos)} new/pending repositories...")
    
    all_results = []
    for repo in pending_repos:
        res = run_traceguard_scan(repo)
        if res:
            all_results.append(res)
            risks_count = res.get('total_containment_risks_detected', 0)
            
            # Record execution permanently in ledger with timestamp
            ledger[repo] = {
                "status": "COMPLETED",
                "scanned_at": datetime.now().isoformat(),
                "risks_detected": risks_count,
                "lead_generated": risks_count > 0
            }
            save_ledger(ledger)

    print("\n[*] Stateful sweep complete. Permanent audit ledger updated.")
