with open("bounty_pipeline.py", "r") as f:
    lines = f.readlines()

# Ensure any 'for line in f' loops have their closing colon
for i, line in enumerate(lines):
    if "for line in f" in line and not line.strip().endswith(":"):
        lines[i] = line.rstrip() + ":\n"

# Safely set candidate slice to 20
for i, line in enumerate(lines):
    if "candidates[:" in line:
        import re
        lines[i] = re.sub(r'candidates\[:\d+\]', 'candidates[:20]', line)

with open("bounty_pipeline.py", "w") as f:
    f.writelines(lines)

print("[+] Syntax fully repaired and batch limit set to 20!")
