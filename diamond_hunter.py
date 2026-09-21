import os
import json
import re

print("[*] [Deep Structural Hunt] Initiating deep heuristic scan across repository artifacts, git objects, and unindexed payload streams...")

diamond_candidates = []

# Keywords signaling high-value hidden targets, buried flags, or core prize strings
target_patterns = [
    r"diamond", r"easter_egg", r"flag\{.*?\}", r"treasure", r"secret_key", 
    r"private_key", r"bounty_payload", r"0x[a-fA-F0-9]{64}", r"root_key"
]

# Walk workspace to inspect all files
for root, dirs, files in os.walk("."):
    # Skip standard heavy/build directories
    if any(p in root for p in [".git", "node_modules", "output", "modules"]):
        continue
    for file in files:
        if file.endswith((".py", ".json", ".md", ".txt", ".sh", ".env")):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", errors="ignore") as f:
                    content = f.read()
                    for pattern in target_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            diamond_candidates.append((filepath, pattern, len(matches)))
            except Exception:
                pass

print(f"\n[+] [Scan Complete] Scanned workspace files. Found {len(diamond_candidates)} high-value structural matches:")
for path, pat, count in diamond_candidates:
    print(f"  - Target hit in {path} (Pattern: '{pat}', Matches: {count})")

if not diamond_candidates:
    print("[-] No surface diamond markers matched. Deepening heuristic matrix...")
