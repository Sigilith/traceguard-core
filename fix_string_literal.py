with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Replace the broken statement line with a clean, single-line string
old_target = '''            "statement": "Choosing to work on Elyan Labs/Rustchain repos because of their focus on sovereign execution and verifiable decentralized protocols."'''
new_target = '            "statement": "Choosing to work on Elyan Labs/Rustchain repos because of their focus on sovereign execution and verifiable decentralized protocols."'

# If exact match fails, let's fix it by searching for the key
if '"statement"' in code:
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if '"statement":' in line and not line.strip().endswith('"'):
            # Combine wrapped lines or make it single line
            lines[i] = '            "statement": "Choosing to work on Elyan Labs/Rustchain repos because of their focus on sovereign execution and verifiable decentralized protocols."'
    code = "\n".join(lines) + "\n"

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] String literal fixed!")
