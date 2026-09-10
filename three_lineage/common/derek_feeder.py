import time
import random
import requests
from pathlib import Path

URL = "https://gardening-bases-licensed-possibilities.trycloudflare.com/"
TARGET_DIRS = ["traceguard-core", "threelineage"]

TIERS = [
    {"tier": "sigilith_core", "amount": 10.00, "desc": "Automated code structure verification"},
    {"tier": "sigilith_audit", "amount": 15.00, "desc": "Symbolic system dependency health check"},
    {"tier": "sigilith_policy", "amount": 20.00, "desc": "Namespace policy engine enforcement scan"}
]

def generate_internal_task():
    selected_dir = random.choice(TARGET_DIRS)
    repo_path = Path.home() / selected_dir
    files = list(repo_path.rglob("*.py"))
    target_file = str(random.choice(files).relative_to(repo_path)) if files else "core_module.py"
    
    tier_info = random.choice(TIERS)
    
    return {
        "client_id": f"internal_audit_{selected_dir}",
        "client_email": "sysadmin@sigilith.local",
        "tier": tier_info["tier"],
        "amount": tier_info["amount"],
        "task_description": f"{tier_info['desc']} on {selected_dir}/{target_file}"
    }

def main():
    print("Derek Internal Work Feeder Active. Dispatching maintenance tasks...")
    while True:
        payload = generate_internal_task()
        try:
            response = requests.post(URL, json=payload, timeout=5)
            print(f"Dispatched: {payload['task_description']} | Response: {response.json()}")
        except Exception as e:
            print(f"Gateway connection error: {e}")
        
        time.sleep(random.randint(30, 60))

if __name__ == "__main__":
    main()
