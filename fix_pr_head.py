import re

with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Replace the payload head definition to use owner:branch for cross-fork PRs
old_payload = '''    payload = {
        "title": f"Fix #{issue_id}: Automated AST Governed Patch for {patch_title}",
        "body": f"Automated solution generated via TraceGuard sovereign execution engine addressing issue #{issue_id}. Verified by ThreeLineage.",
        "head": branch_name,
        "base": "main"
    }'''

new_payload = '''    # For cross-fork PRs, GitHub API requires head to be formatted as "username:branch"
    parts = raw_repo.split('/')
    owner = parts[0]
    head_ref = f"Sigilith:{branch_name}"

    payload = {
        "title": f"Fix #{issue_id}: Automated AST Governed Patch for {patch_title}",
        "body": f"Automated solution generated via TraceGuard sovereign execution engine addressing issue #{issue_id}. Verified by ThreeLineage.",
        "head": head_ref,
        "base": "main"
    }'''

if old_payload in code:
    code = code.replace(old_payload, new_payload)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] PR head reference updated for cross-fork submission!")
else:
    print("[-] Target signature not found, please check file structure.")
