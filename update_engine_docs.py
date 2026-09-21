with open("traceguard_engine.py", "r") as f:
    code = f.read()

# 1. Update function signature to accept repo_slug
code = code.replace(
    'def generate_bounty_payload(issue_id, title, body, sandbox_dir):',
    'def generate_bounty_payload(repo_slug, issue_id, title, body, sandbox_dir):'
)

# 2. Update call site in process_target
code = code.replace(
    'generate_bounty_payload(issue_id, title, body, sandbox_dir)',
    'generate_bounty_payload(raw_repo, issue_id, title, body, sandbox_dir)'
)

with open("traceguard_engine.py", "w") as f:
    f.write(code)

print("[+] Engine signature updated for repo-aware documentation synthesis.")
