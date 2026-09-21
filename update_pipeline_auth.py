import re

with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Replace direct auth URL push with robust credential configuration
old_push = '''        if token and token != "your_github_personal_access_token_here":
            auth_url = repo_url.replace("https://", f"https://x-access-token:{token}@")
            push_res = subprocess.run(["git", "-C", sandbox_dir, "push", auth_url, branch_name])
            if push_res.returncode == 0:
                pr_url = create_github_pr(raw_repo, issue_id, branch_name, title, token)
                if pr_url:
                    status = "PR Submitted & Payout Claimed"'''

new_push = '''        if token and token != "your_github_personal_access_token_here":
            # Configure git credential helper or use token embedded URL for origin
            auth_url = repo_url.replace("https://", f"https://oauth2:{token}@")
            subprocess.run(["git", "-C", sandbox_dir, "remote", "set-url", "origin", auth_url], check=True)
            push_res = subprocess.run(["git", "-C", sandbox_dir, "push", "-u", "origin", branch_name])
            if push_res.returncode == 0:
                pr_url = create_github_pr(raw_repo, issue_id, branch_name, title, token)
                if pr_url:
                    status = "PR Submitted & Payout Claimed"'''

if old_push in code:
    code = code.replace(old_push, new_push)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] bounty_pipeline.py authentication handler updated successfully!")
else:
    print("[-] Signature mismatch, updating push logic manually...")
