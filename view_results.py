import glob
import os
from inspect_ai.log import read_eval_log

# Find the most recent .eval log
log_files = glob.glob("logs/*.eval")
if not log_files:
    print("No evaluation logs found in logs/ directory.")
    exit(1)
    
latest_log = max(log_files, key=os.path.getctime)
print(f"Reading: {latest_log}\n")

# Use Inspect's native parser
log = read_eval_log(latest_log)

for idx, sample in enumerate(log.samples, 1):
    probe_text = str(sample.input)
    
    # Safely extract the score
    score_val = "UNKNOWN"
    reason_val = ""
    if sample.scores and "traceguard_audit" in sample.scores:
        audit_score = sample.scores["traceguard_audit"]
        score_val = audit_score.value
        reason_val = audit_score.explanation

    print(f"[{idx:02d}] State: {score_val:5} | Probe: {probe_text[:40]}...")
    if reason_val:
        print(f"     Reason: {reason_val}")
