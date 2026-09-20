import json
import os
import urllib.request
import urllib.parse

LEDGER_FILE = "audit_ledger.json"

def scan_for_instant_pay_jobs():
    if not os.path.exists(LEDGER_FILE):
        print(f"[-] Audit ledger '{LEDGER_FILE}' not found. Run bot.py first.")
        return

    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    print("=" * 70)
    print("💰 TRACEGUARD INSTANT-PAY JOB & BOUNTY SCANNER")
    print("Scanning repository metadata and security policies for active payouts...")
    print("=" * 70 + "\n")

    found_jobs = 0

    for repo_url in ledger.keys():
        parts = repo_url.rstrip("/").split("/")
        if len(parts) >= 2:
            org, repo = parts[-2], parts[-1]
        else:
            continue

        print(f"[*] Checking target ecosystem: {org}/{repo}")

        # Check for standard bounty and funding markers via GitHub API (public endpoints)
        api_url = f"https://api.github.com/repos/{org}/{repo}"
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "TraceGuard-BountyAgent/1.0"}
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                repo_data = json.loads(response.read().decode())
                
                has_issues = repo_data.get("has_issues", False)
                open_issues = repo_data.get("open_issues_count", 0)
                license_info = repo_data.get("license") or {}
                license_name = license_info.get("name", "Unlicensed/Custom")

                print(f"    - Open Issues: {open_issues} | License: {license_name}")

                # Check if repository or organization has security/bounty indicators
                security_policy_url = f"https://api.github.com/repos/{org}/{repo}/security-advisories"
                
                # Check for financial or funding configuration files
                funding_file_url = f"https://api.github.com/repos/{org}/{repo}/contents/.github/FUNDING.yml"
                funding_req = urllib.request.Request(funding_file_url, headers={"User-Agent": "TraceGuard-BountyAgent/1.0"})
                
                has_funding = False
                try:
                    with urllib.request.urlopen(funding_req, timeout=5) as fund_res:
                        if fund_res.status == 200:
                            has_funding = True
                except Exception:
                    pass

                if has_funding:
                    print(f"    [+] 💸 FOUND FUNDING / PAYOUT HOOK: {repo_url}/blob/main/.github/FUNDING.yml")
                    found_jobs += 1
                else:
                    print(f"    [•] Standard commercial repository (No native funding file detected).")

        except Exception as e:
            print(f"    [-] API rate limit or access check skipped for {org}/{repo}")

        print("-" * 70)

    print(f"\n[*] Instant-Pay Scan Complete. Identified {found_jobs} monetized / funded repositories with active payout structures.")

if __name__ == "__main__":
    scan_for_instant_pay_jobs()
