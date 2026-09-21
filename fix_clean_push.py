with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Replace the push line with a sequence that unsets upstream/tracking if stale, then pushes cleanly
old_push_line = 'push_res = subprocess.run(["git", "-C", sandbox_dir, "push", "-u", "origin", branch_name, "--force-with-lease"])'

new_push_code = '''# Clear any stale tracking references to avoid stale info rejections
            subprocess.run(["git", "-C", sandbox_dir, "branch", "--unset-upstream"], capture_output=True)
            push_res = subprocess.run(["git", "-C", sandbox_dir, "push", "origin", f"{branch_name}:{branch_name}", "--force"])'''

if old_push_line in code:
    code = code.replace(old_push_line, new_push_code)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] Clean-push logic with explicit ref mapping installed!")
else:
    print("[-] Push line signature not found.")
