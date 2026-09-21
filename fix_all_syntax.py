with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Clean all corrupted variable or file handle definitions
code = code.replace("as f[[:20]20]", "as f:")
code = code.replace("as f[:20]", "as f:")
code = code.replace("ledger_file)[[:20]20]", "ledger_file):")

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] All syntax errors cleared!")
