import os
import hashlib
import time
import subprocess

WATCH_DIR = os.path.expanduser("~/three-lineage-core/.lineage")
BASELINE = {}

def hash_file(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def build_baseline():
    os.makedirs(WATCH_DIR, exist_ok=True)
    for root, _, files in os.walk(WATCH_DIR):
        for file in files:
            path = os.path.join(root, file)
            h = hash_file(path)
            if h:
                BASELINE[path] = h
    print(f"[+] Baseline secured: Tracking {len(BASELINE)} files.")

def notify(message):
    print(f"[ALERT] {message}")
    subprocess.run(["notify-send", "Security Alert", message], capture_output=True)

def monitor_loop():
    build_baseline()
    while True:
        time.sleep(10)
        current_files = set()
        for root, _, files in os.walk(WATCH_DIR):
            for file in files:
                path = os.path.join(root, file)
                current_files.add(path)
                h = hash_file(path)
                
                if path not in BASELINE:
                    notify(f"New unauthorized file detected: {file}")
                    BASELINE[path] = h
                elif BASELINE[path] != h:
                    notify(f"INTEGRITY BREACH: File modified -> {file}")
                    BASELINE[path] = h
                    
        for path in list(BASELINE.keys()):
            if path not in current_files:
                notify(f"File deleted: {os.path.basename(path)}")
                del BASELINE[path]

if __name__ == "__main__":
    monitor_loop()
