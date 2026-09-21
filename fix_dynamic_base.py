with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Replace static base branch with dynamic lookup from GitHub API
old_payload_section = '''    payload = {
        "title": f"Fix #{issue_id}: Automated AST Governed Patch for {patch_title}",
        "body": f"Automated solution generated via TraceGuard sovereign execution engine addressing issue #{issue_id}. Verified by ThreeLineage.",
        "head": head_ref,
        "base": "main"
    }'''

new_payload_section = '''    # Dynamically fetch the target repository's default branch (e.g., master vs main)
    base_branch = "main"
    try:
        repo_api_url = f"https://api.github.com/repos/{repo_slug}"
        repo_req = urllib.request.Request(
            repo_api_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "TraceGuard-Autonomous-Agent"
            }
        )
        with urllib.request.urlopen(repo_req) as r:
            repo_meta = json.loads(r.read().decode())
            base_branch = repo_meta.get("default_branch", "main")
            print(f"[*] [PaymentBot] Detected upstream default branch: '{base_branch}'")
    except Exception as be:
        print(f"[*] [PaymentBot] Could not fetch default branch, falling back to 'main': {be}")

    payload = {
        "title": f"Fix #{issue_id}: Automated AST Governed Patch for {patch_title}",
        "body": f"Automated solution generated via TraceGuard sovereign execution engine addressing issue #{issue_id}. Verified by ThreeLineage.",
        "head": head_ref,
        "base": base_branch
    }'''

if old_payload_section in code:
    code = code.replace(old_payload_section, new_payload_section)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] Dynamic base branch resolution installed successfully!")
else:
    print("[-] Target payload section not found.")
