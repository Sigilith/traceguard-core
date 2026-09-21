with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Clean up any malformed bracket injections from the previous script
code = code.replace("if os.path.exists(ledger_file)[[:20]20]", "if os.path.exists(ledger_file):")
code = code.replace("if os.path.exists(ledger_file)[[:20]]", "if os.path.exists(ledger_file):")
code = code.replace("if os.path.exists(ledger_file)[:20]", "if os.path.exists(ledger_file):")

# Safely target candidate iteration or slicing (e.g., changing [:5] or max 5 limits to 20)
code = code.replace("candidates[:5]", "candidates[:20]")

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Syntax fully cleaned and restored!")
