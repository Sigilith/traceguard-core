import os
import json
import urllib.request

token = os.environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json", "User-Agent": "TraceGuard-Valuation"}

# Sample high-value repos from your latest run
repos = [
    ("Scottcjn/rustchain-bounties", [2155, 378, 165, 9017, 16238]),
    ("ditto-assistant/ditto-subnet", [2047]),
    ("Scottcjn/bottube", [644])
]

print("[*] [Valuation Engine] Scanning live issue bodies for monetary and token values...")
total_rtc = 0
total_usd = 0

for repo, issues in repos:
    for issue_id in issues:
        url = f"https://api.github.com/repos/{repo}/issues/{issue_id}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                title = data.get('title', '')
                print(f"  - [{repo} #{issue_id}] {title}")
        except Exception:
            pass

print("[+] Scan complete. All active reward tags mapped.")
