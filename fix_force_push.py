with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Replace standard push with force-with-lease for personal forks
old_push_cmd = 'push_res = subprocess.run(["git", "-C", sandbox_dir, "push", "-u", "origin", branch_name])'
new_push_cmd = 'push_res = subprocess.run(["git", "-C", sandbox_dir, "push", "-u", "origin", branch_name, "--force-with-lease"])'

if old_push_cmd in code:
    code = code.replace(old_push_cmd, new_push_cmd)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] Safe force-push logic installed successfully!")
else:
    print("[-] Push command signature not found.")
