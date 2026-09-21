with open("bounty_pipeline.py", "r") as f:
    lines = f.readlines()

new_lines = []
keywords = ("if ", "elif ", "for ", "def ", "else", "try", "except", "with ", "while ")

for line in lines:
    stripped = line.strip()
    # Check if line starts with a python control keyword and doesn't end with a colon (ignoring inline comments)
    if any(stripped.startswith(kw) for kw in keywords) and not stripped.endswith(":") and not "#" in stripped:
        # Retain original indentation
        indent = line[:len(line) - len(line.lstrip())]
        fixed_line = indent + stripped + ":\n"
        new_lines.append(fixed_line)
    else:
        new_lines.append(line)

with open("bounty_pipeline.py", "w") as f:
    f.writelines(new_lines)

print("[+] All missing colons automatically restored across bounty_pipeline.py!")
