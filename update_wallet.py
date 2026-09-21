import json
import os

wallet_address = "0x58d30dc1759f78b3ffd98460c025000de7d218bc"
config_path = "config_state.json"

# Load or initialize config state
config = {}
if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        config = {}

config["payout_wallet"] = wallet_address

with open(config_path, "w") as f:
    json.dump(config, f, indent=4)

print(f"[+] [Config] Wallet address {wallet_address} successfully locked into {config_path}.")
