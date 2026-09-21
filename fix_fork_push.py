import re

with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Replace direct origin push with fork-aware remote mapping
old_push_logic = '''        if token and token != "your_github_personal_access_token_here":
            # Configure git credential helper or use token embedded URL for origin
            auth_url = repo_url.replace("https://", f"https://oauth2:{token}@")
            subprocess.run(["git", "-C", sandbox_dir, "remote", "set-url", "origin", auth_url], check=True)
            push_res = subprocess.run(["git", "-C", sandbox_dir, "push", "-u", "origin", branch_name])'''

new_push_logic = '''        if token and token != "your_github_personal_access_token_here":
            # Remap origin to user's personal fork space or handle via token auth
            parts = raw_repo.split('/')
            owner, repo_name = parts[0], parts[1]
            # If not owned by user, map origin to personal fork or push with token
            fork_repo = f"Sigilith/{repo_name}"
            fork_url = f"https://oauth2:{token}@github.com/{fork_repo}.git"
            
            print(f"[*] [PaymentBot] Targeting personal fork workspace: {fork_repo}")
            subprocess.run(["git", "-C", sandbox_dir, "remote", "set-url", "origin", fork_url], check=True)
            push_res = subprocess.run(["git", "-C", sandbox_dir, "push", "-u", "origin", branch_name])'''

if old_push_logic in code:
    code = code.replace(old_push_logic, new_push_logic)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] Fork-aware push logic installed successfully!")
else:
    print("[-] Target signature not found, please check file structure.")
