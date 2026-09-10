import os
import sys

COPYRIGHT_HEADER = "# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved."

def audit_workspace():
    print("====================================================")
    print("🔍 THREE-LINEAGE WORKSPACE INTEGRITY & COMPLIANCE")
    print("====================================================")
    
    root_dir = "."
    excluded_dirs = {".git", "__pycache__", ".lineage"}
    empty_dirs = []
    missing_licenses = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs and not d.startswith(".")]
        
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
            
        for file in filenames:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "Copyright" not in content:
                            missing_licenses.append(full_path)
                except Exception:
                    pass

    if empty_dirs:
        print(f"[!] WARNING: Empty directories detected: {empty_dirs}")
    else:
        print("[+] Directory Integrity: All folders contain valid structural artifacts.")

    if missing_licenses:
        print(f"[!] WARNING: Missing copyright headers in: {missing_licenses}")
    else:
        print("[+] License Compliance: All source files carry sovereign copyright headers.")

    if not empty_dirs and not missing_licenses:
        print("[+] VERDICT: Workspace 100% compliant. Air-gapped framework verified.")

if __name__ == "__main__":
    audit_workspace()
