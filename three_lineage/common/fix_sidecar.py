with open("three_lineage_sidecar.py", "r") as f:
    content = f.read()

# Replace Python default spacing with compact separators matching Rust
old_code = 'canonical_data = json.dumps(event, sort_keys=True)'
new_code = 'canonical_data = json.dumps(event, sort_keys=True, separators=(",", ":"))'

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("three_lineage_sidecar.py", "w") as f:
        f.write(content)
    print("[+] Sidecar updated with explicit compact JSON canonicalization.")
else:
    print("[!] Target string not found, checking manual replacement.")
