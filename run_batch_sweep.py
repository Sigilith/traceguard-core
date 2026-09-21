import subprocess

print("[+] [Accelerator] Initiating high-value multi-ecosystem batch sweep...")
# Execute the core traceguard hunt and submission engine for the next batch
subprocess.run(["python3", "master_pipeline.py", "--batch-tier", "high", "--target-count", "6"], capture_output=False)
print("[+] [Accelerator] Batch sweep cycle deployed and active.")
