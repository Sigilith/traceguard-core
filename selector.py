import os
import sys
import subprocess
import shutil

def run_targeted_audit():
    target = None
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    clone_dir = "./live_target_audit"
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)

    if target:
        if target.startswith("http://") or target.startswith("https://") or target.endswith(".git"):
            print(f"🤖 [BOT TARGETED SCOUT]: Cloning custom target -> {target}")
            try:
                subprocess.run(["git", "clone", "--depth", "1", target, clone_dir], check=True)
                scan_path = clone_dir
            except subprocess.CalledProcessError:
                print(f"[-] Error: Failed to clone repository. Please check the URL and try again.")
                return
        else:
            print(f"🤖 [BOT TARGETED SCOUT]: Locking onto local path -> {target}")
            scan_path = target
    else:
        print("🤖 [BOT TARGETED SCOUT]: No target specified. Defaulting to workspace.")
        scan_path = os.getcwd()

    print(f"\n=======================================================================")
    print(f"🚀 LAUNCHING MULTI-STREAM PIPELINE ON TARGET")
    print(f"=======================================================================")
    subprocess.run(["python3", "bot.py", "--local", scan_path])

if __name__ == "__main__":
    run_targeted_audit()
