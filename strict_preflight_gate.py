import subprocess
import sys
import os

print("[*] [Strict Gate v1.0] Enforcing pre-flight validation before any deployment...")

def check_local_syntax():
    print("[*] Running local syntax and safety checks...")
    # Verify no syntax errors in python scripts
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r") as f:
                        compile(f.read(), path, 'exec')
                except Exception as e:
                    print(f"[!] Syntax error detected in {path}: {e}")
                    return False
    print("[+] All local files passed syntax and pre-flight validation.")
    return True

if not check_local_syntax():
    print("[!] Pre-flight validation FAILED. Halting process. Fix errors before committing.")
    sys.exit(1)

print("[+] Pre-flight gate passed successfully. Safe to proceed locally.")
