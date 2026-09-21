import re

with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Locate where fork_repo is defined and add GitHub API fork creation call before setting remote url
target_snippet = '''            parts = raw_repo.split('/')
            owner, repo_name = parts[0], parts[1]
            # If not owned by user, map origin to personal fork or push with token
            fork_repo = f"Sigilith/{repo_name}"
            fork_url = f"https://oauth2:{token}@github.com/{fork_repo}.git"'''

enhanced_snippet = '''            parts = raw_repo.split('/')
            owner, repo_name = parts[0], parts[1]
            
            # Automatically create fork via GitHub API if it doesn't exist yet
            print(f"[*] [PaymentBot] Ensuring personal fork exists for {raw_repo}...")
            fork_api_url = f"https://api.github.com/repos/{raw_repo}/forks"
            fork_req = urllib.request.Request(
                fork_api_url,
                data=b"{}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json",
                    "User-Agent": "TraceGuard-Autonomous-Agent"
                },
                method="POST"
            )
            try:
                with urllib.request.urlopen(fork_req) as fork_resp:
                    print(f"[+] [PaymentBot] Fork verified / created successfully.")
            except Exception as fe:
                print(f"[*] [PaymentBot] Note on fork creation (may already exist): {fe}")

            fork_repo = f"Sigilith/{repo_name}"
            fork_url = f"https://oauth2:{token}@github.com/{fork_repo}.git"'''

if target_snippet in code:
    code = code.replace(target_snippet, enhanced_snippet)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] Auto-forking API logic installed successfully!")
else:
    print("[-] Target signature not found, checking alternative pattern...")
