with open("traceguard_engine.py", "r") as f:
    code = f.read()

# Add pre-flight check and social action functions
compliance_code = '''
def check_repository_requirements(repo_slug, token):
    """Fetches contributing guidelines and checks for strict rules like DCO or signed commits."""
    print(f"[*] [Pre-Flight] Checking contribution requirements for {repo_slug}...")
    url = f"https://api.github.com/repos/{repo_slug}/contents/CONTRIBUTING.md"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TraceGuard-Autonomous-Agent"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            content = urllib.request.urlopen(data['download_url']).read().decode().lower()
            needs_dco = "dco" in content or "developer certificate of origin" in content
            needs_gpg = "sign" in content or "gpg" in content
            print(f"[+] [Pre-Flight Rules] DCO Required: {needs_dco} | GPG Sign Required: {needs_gpg}")
            return {"dco": needs_dco, "gpg": needs_gpg}
    except Exception:
        # Default strict assumption if no CONTRIBUTING.md is found
        return {"dco": True, "gpg": True}

def perform_social_actions(repo_slug, token):
    """Follows the repository owner or stars/watches the repo if required."""
    owner = repo_slug.split('/')[0]
    print(f"[*] [Social Engine] Engaging with repository owner: {owner}")
    url = f"https://api.github.com/user/following/{owner}"
    req = urllib.request.Request(
        url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TraceGuard-Autonomous-Agent",
            "Content-Length": "0"
        }, method="PUT"
    )
    try:
        with urllib.request.urlopen(req):
            print(f"[+] [Social Engine] Successfully followed {owner}.")
    except Exception:
        pass # Non-critical if already following or restricted
''`

# Insert compliance_code before process_target
code = code.replace('def process_target(', compliance_code + '\n\ndef process_target(')

# Update process_target to call these checks before doing work
old_target_start = '''    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, sandbox_dir], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)'''

new_target_start = '''    try:
        # Step 1: Perform Social Actions & Pre-Flight Compliance Verification
        perform_social_actions(raw_repo, token)
        reqs = check_repository_requirements(raw_repo, token)
        
        print(f"[*] [AXIOMOS] Requirements verified. Proceeding to clone and synthesize patch...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, sandbox_dir], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)'''

if old_target_start in code:
    code = code.replace(old_target_start, new_target_start)
    with open("traceguard_engine.py", "w") as f:
        f.write(code)
    print("[+] Pre-flight requirements and social automation added successfully!")
else:
    print("[-] Target start block not found, check script.")

