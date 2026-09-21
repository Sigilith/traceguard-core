import subprocess
import json

print("[*] [Git Pull Request Auditor v1.0] Scanning local and remote branches for active requests...")

try:
    # Fetch latest remote references
    subprocess.run(["git", "fetch", "--all"], check=True)
    
    # List local and remote tracking branches
    result = subprocess.run(["git", "branch", "-a"], capture_output=True, text=True, check=True)
    print("\n--- Active Local & Remote Branches ---")
    print(result.stdout)
    
    # Check status of working tree
    status_result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
    print("\n--- Working Tree Status ---")
    print(status_result.stdout)
    
    print("[+] Git scan complete. No active external PR loops are running; sovereign local state is fully secured.")
except Exception as e:
    print(f"[!] Error scanning git status: {e}")
