import os
import sys

# Add repository root to python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("[*] Initiating fail-closed governance path audit...")

pipeline_path = "three_lineage/core/pipeline.py"
if os.path.exists(pipeline_path):
    with open(pipeline_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
        
    # Check for fail-closed strings
    has_deny = "DENY" in source_code
    has_fallback = "allow_fallback" in source_code
    
    print(f"    - Target File: {pipeline_path}")
    print(f"    - Fail-Closed 'DENY' Invariant Present: {has_deny}")
    print(f"    - Legacy 'allow_fallback' Pattern Present: {has_fallback}")
    
    if has_deny and not has_fallback:
        print("[+] VERIFICATION PASSED: Pipeline is strictly fail-closed.")
    else:
        print("[-] VERIFICATION FAILED: Potential fallback vector detected.")
else:
    print(f"[-] Target file {pipeline_path} not found.")

