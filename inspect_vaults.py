import json
import os

vaults = ["vault_boundary_live.dat", "vault_fuzz.dat", "vault_chaotic_storm.dat", "vault_live_soak.dat"]

for vfile in vaults:
    if os.path.exists(vfile):
        with open(vfile, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
            if lines:
                last_block = json.loads(lines[-1])
                block_hash = last_block.get("block_hash", "N/A")[:12]
                print(f"[VAULT] {vfile:<25} | Blocks: {len(lines):<5} | Head Hash: {block_hash}...")
