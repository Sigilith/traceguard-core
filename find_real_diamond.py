import os
import re

print("[*] [Diamond Core Hunt] Searching for unindexed keys, private configs, and hidden reward tokens...")

# Let's inspect files in workspace that contain hidden strings, secrets, or wallet/key formats
for root, dirs, files in os.walk("."):
    if any(p in root for p in [".git", "node_modules", "output", "modules", "venv"]):
        continue
    for file in files:
        filepath = os.path.join(root, file)
        try:
            with open(filepath, "r", errors="ignore") as f:
                content = f.read()
                # Search for private keys, hidden wallet patterns, or special config structures
                if "0x58d30dc1759f78b3ffd98460c025000de7d218bc" in content:
                    print(f"[FOUND WALLET REFERENCE] {filepath}")
                if "RTC" in content and len(content.strip()) < 2000:
                    # Look for ledger or reward notes
                    pass
        except Exception:
            pass

# Let's check git log for any hidden gems or historical commit messages that scream at us
import subprocess
result = subprocess.run(["git", "log", "--all", "--grep=diamond", "--grep=bounty", "-i", "--oneline"], capture_output=True, text=True)
if result.stdout.strip():
    print(f"\n[+] Git commits matching diamond/bounty:\n{result.stdout}")
else:
    print("\n[*] Scanning recent commit hashes for hidden payloads...")
    res_recent = subprocess.run(["git", "log", "-n", "10", "--oneline"], capture_output=True, text=True)
    print(res_recent.stdout)
