import os
import re

for root, dirs, files in os.walk("."):
    if any(p in root for p in [".git", "node_modules", "output", "modules", "venv"]):
        continue
    for file in files:
        filepath = os.path.join(root, file)
        try:
            with open(filepath, "r", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    if "diamond" in line.lower() or "bounty_payload" in line.lower():
                        print(f"{filepath}:{line_num} -> {line.strip()}")
        except Exception:
            pass
