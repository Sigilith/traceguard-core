with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Completely scrub all malformed bracket artifacts introduced by previous scripts
code = code.replace("[[:20]20]", "")
code = code.replace("[:20]20", "")
code = code.replace("[[:20]]", "")

# Safely update candidates limit from 5 to 20 if present
code = code.replace("candidates[:5]", "candidates[:20]")

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] All file corruptions scrubbed!")
