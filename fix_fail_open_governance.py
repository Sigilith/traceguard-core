import os
import re

print("[*] Scanning codebase for fail-open 'allow_fallback' patterns...")
patched_files = 0

for root, dirs, files in os.walk("three_lineage"):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            if "allow_fallback" in content:
                print(f"[!] Found fail-open pattern in: {filepath}")
                # Replace allow_fallback with strict deny / fail-closed invariant
                new_content = re.sub(
                    r'"decision":\s*"allow_fallback"',
                    '"decision": "DENY", "reason": "GOVERNANCE_EXCEPTION_FAIL_CLOSED"',
                    content
                )
                new_content = re.sub(
                    r"'decision':\s*'allow_fallback'",
                    "'decision': 'DENY', 'reason': 'GOVERNANCE_EXCEPTION_FAIL_CLOSED'",
                    new_content
                )
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"[+] Patched {filepath} to fail closed.")
                    patched_files += 1

print(f"[*] Remediation complete. Total files patched: {patched_files}")
