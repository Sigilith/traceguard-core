with open("bounty_pipeline.py", "r") as f:
    lines = f.readlines()

# Ensure line 16 (or any line starting with 'if ...') has its closing colon
if len(lines) >= 16:
    target_line = lines[15] # 0-indexed for line 16
    if "startswith" in target_line and not target_line.strip().endswith(":"):
        lines[15] = target_line.rstrip() + ":\n"

with open("bounty_pipeline.py", "w") as f:
    f.writelines(lines)

print("[+] Line 16 colon fixed!")
