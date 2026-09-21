with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Fix the function signature and call to accept repo_slug
old_def = "def create_github_pr(repo_slug, issue_id, branch_name, patch_title, token):"
# Inside create_github_pr, replace the raw_repo split logic with the passed repo_slug argument
old_head_logic = '''    # For cross-fork PRs, GitHub API requires head to be formatted as "username:branch"
    parts = raw_repo.split('/')
    owner = parts[0]
    head_ref = f"Sigilith:{branch_name}"'''

new_head_logic = '''    # For cross-fork PRs, GitHub API requires head to be formatted as "username:branch"
    parts = repo_slug.split('/')
    owner = parts[0]
    head_ref = f"Sigilith:{branch_name}"'''

code = code.replace(old_head_logic, new_head_logic)

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Scope bug fixed! `repo_slug` is now correctly referenced in PR creation.")
