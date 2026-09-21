with open("traceguard_engine.py", "r") as f:
    code = f.read()

# Revert git commit command to use only DCO sign-off (-s) instead of requiring GPG (-S)
old_commit = 'subprocess.run(["git", "-C", sandbox_dir, "commit", "-s", "-S", "-m", f"fix: automated patch for issue #{issue_id}"], check=True, stdout=subprocess.DEVNULL)'
new_commit = 'subprocess.run(["git", "-C", sandbox_dir, "commit", "-s", "-m", f"fix: automated patch for issue #{issue_id}"], check=True, stdout=subprocess.DEVNULL)'

if old_commit in code:
    code = code.replace(old_commit, new_commit)
    with open("traceguard_engine.py", "w") as f:
        f.write(code)
    print("[+] Removed strict GPG requirement (-S), keeping DCO sign-off (-s).")
else:
    print("[-] Commit line mismatch, check script.")

