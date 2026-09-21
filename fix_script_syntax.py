with open("traceguard_engine.py", "r") as f:
    code = f.read()

# Make sure we don't have duplicate preflight functions if it partially applied
if "def check_repository_requirements" not in code:
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
        pass
'''
    code = compliance_code + "\n\n" + code
    with open("traceguard_engine.py", "w") as f:
        f.write(code)
    print("[+] Pre-flight and social functions injected cleanly.")
else:
    print("[*] Pre-flight functions already present.")

