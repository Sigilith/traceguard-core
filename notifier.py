import urllib.request
import urllib.parse
import json
import os

def dispatch_github_security_issue(repo_url, risk_count):
    """Programmatically opens a security advisory issue on target repositories via GitHub API."""
    github_token = os.environ.get("GITHUB_TOKEN", "")
    if not github_token:
        print("[-] GitHub token not found. Set GITHUB_TOKEN environment variable to enable automated issue posting.")
        return False
        
    # Convert https://github.com/owner/repo to owner/repo format
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        return False
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    issue_title = "🛡️ Security Advisory: Structural Containment Risks Isolated"
    issue_body = (
        f"Hello maintainers,\n\n"
        f"TraceGuard automated structural security engine scanned this repository and isolated **{risk_count} structural containment risk(s)** "
        f"(including potential dynamic execution vectors or exposed credentials).\n\n"
        f"To view the full line-by-line remediation patch and security breakdown, access the verified audit report here:\n"
        f"👉 https://traceguard-web.onrender.com/pay\n\n"
        f"*(Automated security notification by TraceGuard Intelligence)*"
    )
    
    payload = json.dumps({
        "title": issue_title,
        "body": issue_body,
        "labels": ["security", "vulnerability"]
    }).encode('utf-8')
    
    req = urllib.request.Request(
        api_url,
        data=payload,
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "TraceGuard-Security-Bot"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode())
            print(f"[+] Successfully posted GitHub security issue for {repo_url}: {res_data.get('html_url')}")
            return True
    except Exception as e:
        print(f"[-] Failed to post GitHub issue for {repo_url}: {e}")
        return False
