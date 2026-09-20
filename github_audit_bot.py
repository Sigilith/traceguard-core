import os
import sys
import requests
from datetime import datetime

sys.path.append("audit_sandbox")

try:
    from controlarena_submission_wrapper import gate_command
except ImportError:
    print("[-] Error: TraceGuard engine not found in audit_sandbox.")
    sys.exit(1)

TARGET_QUERIES = [
    "pickle.loads language:python",
    "exec( language:python",
    "eval( language:python"
]

PAYPAL_CHECKOUT_LINK = "https://paypal.me/yourname/49"

def generate_markdown_report(repo_name, file_url, state, reason, snippet):
    os.makedirs("audit_reports", exist_ok=True)
    safe_name = repo_name.replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audit_reports/Audit_{safe_name}_{timestamp}.md"
    
    report_content = f'''# TraceGuard V3: Security Vulnerability Audit

- **Repository:** `{repo_name}`
- **Source File:** {file_url}
- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Engine Status:** AXIOMOS AST Governance (`{state}`)

## Executive Summary
TraceGuard V3 intercepted an unauthorized execution vector during automated parsing. This pattern represents a critical risk profile.

### Triggered Code Sample
```python
{snippet}
```

### Governance Verdict
- **Classification:** **{state}**
- **Analysis:** {reason}

---

## Unlock Full Remediation & Patch
To access the automated AST containment boundary patch and full security remediation guide for this repository, complete the evaluation fee (£49):

👉 **[Pay via PayPal and Unlock Report]({PAYPAL_CHECKOUT_LINK})**

*Once payment is verified, your sovereign execution boundary configuration file will be dispatched.*
'''
    with open(filename, "w") as f:
        f.write(report_content)
    print(f"[+] Generated client-ready report: {filename}")

def scan_github_snippets():
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        print("[+] Using authenticated GitHub session.")
    else:
        print("[!] Error: GITHUB_TOKEN environment variable required.")
        return

    print("=" * 60)
    for query in TARGET_QUERIES:
        print(f"[*] Querying GitHub for pattern: '{query}'...")
        url = f"https://api.github.com/search/code?q={query}&per_page=2"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"[-] API Error ({response.status_code}): {response.text}")
            continue

        items = response.json().get("items", [])
        for item in items:
            file_url = item.get("html_url")
            repo_name = item.get("repository", {}).get("full_name")
            
            raw_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            raw_res = requests.get(raw_url)
            code_snippet = raw_res.text if raw_res.status_code == 200 else "import unsafe_fallback"

            probe = {"node_id": f"github_audit_{repo_name}", "code": code_snippet[:600]}
            res = gate_command(probe)
            state = res.get("state", "UNKNOWN")
            reason = res.get("reason", "No reason provided.")

            print(f"    -> Repo: {repo_name} | Verdict: {state}")
            
            if state == "RED":
                generate_markdown_report(repo_name, file_url, state, reason, code_snippet[:400])

    print("=" * 60)
    print("[+] Scan complete. Check the 'audit_reports/' folder for generated assets.")

if __name__ == "__main__":
    scan_github_snippets()
