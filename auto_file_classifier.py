import os
import shutil

ROOT = os.getcwd()
MODULES = {
    "aximos": "three_lineage/aximos",
    "traceguard": "three_lineage/traceguard",
    "sigilith": "three_lineage/sigilith",
    "common": "three_lineage/common"
}

def classify_file(path):
    with open(path, "r", errors="ignore") as f:
        content = f.read()

    if "AXIOMOS" in content or "whitelist" in content or "governance" in content:
        return "aximos"
    if "TraceGuard" in content or "execution" in content or "sandbox" in content:
        return "traceguard"
    if "Sigilith" in content or "stability" in content or "symbolic" in content:
        return "sigilith"
    return "common"

def auto_sort():
    print("[*] Auto-Sort Engine: Scanning for new files...")

    for fname in os.listdir(ROOT):
        if fname.endswith(".py") and fname not in [
            "auto_file_classifier.py",
            "fetch_threat_signatures.py",
            "test_sentinel_block.py",
            "prod_start.sh"
        ]:
            src = os.path.join(ROOT, fname)
            module = classify_file(src)
            dst_dir = MODULES[module]
            dst = os.path.join(dst_dir, fname)

            print(f"[+] Sorting {fname} → {module}")
            shutil.move(src, dst)

    print("[✓] Auto-Sort Complete. All new files placed correctly.")

if __name__ == "__main__":
    auto_sort()
