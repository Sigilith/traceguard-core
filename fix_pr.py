import os
import subprocess

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "traceguard-core" in content or "🛡️" in content:
                print(f"[*] Updating references in {path}")
                new_content = content.replace("Sigilith/traceguard-core", "traceguard-core") # Prevent double prefixing if partial
                new_content = content.replace("traceguard-core", "Sigilith/traceguard-core")
                new_content = new_content.replace("🛡️", "🐍")
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)

subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "fix: update entry to Sigilith/traceguard-core and replace emoji with 🐍"])
subprocess.run(["git", "push"])
print("[+] Terminal modifications committed and pushed.")
