import os
import shutil
import zipfile

bundle_dir = "dist/traceguard_v3_submission_bundle"
zip_file = "dist/traceguard_v3_controlarena_bundle.zip"

if os.path.exists(bundle_dir):
    shutil.rmtree(bundle_dir)
os.makedirs(bundle_dir)

# File manifest for submission
files_to_copy = [
    ("engine/controlarena_submission_wrapper.py", "controlarena_submission_wrapper.py"),
    ("engine/traceguard_v3_expanded.py", "traceguard_v3_expanded.py"),
    ("engine/telemetry_dashboard.py", "telemetry_dashboard.py"),
    ("engine/test_protocol.py", "test_protocol.py"),
    ("Dockerfile", "Dockerfile"),
    ("docker-compose.yml", "docker-compose.yml"),
    ("requirements.txt", "requirements.txt")
]

for src, dst in files_to_copy:
    if os.path.exists(src):
        shutil.copy(src, os.path.join(bundle_dir, dst))

# Create Manifest file
manifest_content = """===============================================================================
TRACEGUARD V3 // CONTROL ARENA SUBMISSION MANIFEST
===============================================================================
Protocol Name : TraceGuard V3 Governance Runtime
Version       : 3.0.0
Author        : Sigilith-labs // ThreeLineage Research Group
Entrypoint    : controlarena_submission_wrapper.py
Function      : gate_command(payload: dict) -> dict

INCLUDED FILES:
- controlarena_submission_wrapper.py : ControlArena interface & ledger verifier.
- traceguard_v3_expanded.py           : AXIOMOS AST visitor core & V3 arena.
- telemetry_dashboard.py              : Visual analytics & SIEM telemetry parser.
- test_protocol.py                    : Integration verification suite.
- Dockerfile & docker-compose.yml     : Isolated container execution profiles.
===============================================================================
"""

with open(os.path.join(bundle_dir, "MANIFEST.txt"), "w") as f:
    f.write(manifest_content)

# Package into ZIP archive
with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(bundle_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, bundle_dir)
            zipf.write(file_path, arcname)

print("\n" + "="*70)
print("  TRACEGUARD V3 SUBMISSION BUNDLE GENERATED")
print("="*70)
print(f"  Directory : {bundle_dir}")
print(f"  Archive   : {zip_file}")
print("="*70 + "\n")
