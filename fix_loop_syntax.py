with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Fix corrupted loop iterations or object slicing
code = code.replace("for line in f[[:20]20]:", "for line in f:")
code = code.replace("for line in f[:20]:", "for line in f:")
code = code.replace("for line in f[[:20]20]", "for line in f")

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Loop syntax cleaned successfully!")
