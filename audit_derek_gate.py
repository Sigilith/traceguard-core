import os

# Locate Derek gate implementation files across the repository
gate_files = []
for root, dirs, files in os.walk("three_lineage"):
    for file in files:
        if "derek" in file or "gate" in file:
            gate_files.append(os.path.join(root, file))

print(f"[*] Discovered Derek/Gate components: {gate_files}")

for filepath in gate_files:
    print(f"\n--- Inspecting: {filepath} ---")
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if "fallback" in content.lower() or "allow" in content.lower():
            print("[!] Found policy decision keywords.")
            lines = content.splitlines()
            for idx, line in enumerate(lines):
                if any(kw in line.lower() for kw in ["fallback", "allow", "deny", "halt", "fail"]):
                    print(f"    Line {idx+1}: {line.strip()}")
        else:
            print("    [+] No fallback/allow logic detected in this file.")
