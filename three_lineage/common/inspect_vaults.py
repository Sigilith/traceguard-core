import os, json

VAULT_PREFIX = "vault_"

def safe_json_load(line):
    try:
        return json.loads(line)
    except Exception:
        return None

for fname in os.listdir("."):
    if fname.startswith(VAULT_PREFIX) and fname.endswith(".dat"):
        print(f"[VAULT] {fname}")

        try:
            with open(fname, "r") as f:
                lines = f.read().splitlines()
        except Exception as e:
            print(f"[ERROR] Could not read {fname}: {e}")
            continue

        if not lines:
            print(f"[EMPTY] {fname} contains no blocks.")
            continue

        last_line = lines[-1]
        parsed = safe_json_load(last_line)

        if parsed is None:
            print(f"[SKIP] {fname} contains encrypted or non‑JSON evidence. Inspector will not parse this vault.")
            continue

        # JSON vault: show block count + head hash
        print(f"  Blocks: {len(lines)}")
        print(f"  Head Hash: {parsed.get('block_hash', 'UNKNOWN')}")
