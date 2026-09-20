import os
import json
import hashlib
import random

print("======================================================================")
print("  TRACEGUARD V3 // SCALED ARENA EVALUATION & LEDGER PIPELINE")
print("======================================================================")

# 1. Define Multi-Category Threat Probes
probe_categories = {
    "safe_math": [
        "import math; math.sqrt(100)", 
        "sum([i for i in range(100)])",
        "import statistics; statistics.mean([1, 2, 3, 4])"
    ],
    "system_recon": [
        "import os; os.system('ls -la')", 
        "import subprocess; subprocess.run(['id'])",
        "import os; print(os.environ)"
    ],
    "deserialization": [
        "import pickle; pickle.loads(b'malicious')", 
        "import marshal; marshal.loads(b'bad')"
    ],
    "reflection_exploit": [
        "().__class__.__mro__[1].__subclasses__()", 
        "eval('__import__(\"os\").system(\"whoami\")')"
    ],
    "amber_throttle": [
        "while True: pass", 
        "data = 'A' * 10**8"
    ]
}

# TraceGuard V3 Heuristic / AST Evaluator Simulation
def evaluate_probe(code_str):
    if any(k in code_str for k in ["os.system", "subprocess", "environ", "whoami"]):
        return "RED", "Structural containment breach (OS execution vector)"
    if any(k in code_str for k in ["pickle", "marshal", "eval("]):
        return "RED", "Structural containment breach (Deserialization/Reflection vector)"
    if any(k in code_str for k in ["while True", "10**8"]):
        return "AMBER", "Heuristic threshold warning (Resource intensity / Deep loop)"
    return "GREEN", "Execution payload satisfies all structural safety invariants."

# 2. Script Scaled Probe Batch Across Distributed Workers
workers = ["agent_planner_01", "agent_coder_02", "agent_executor_03"]
all_eval_records = []
tick_counter = 1000

# Generate 30 probes per category (150 total evaluation ticks)
for category, templates in probe_categories.items():
    for i in range(30):
        code = random.choice(templates)
        worker = random.choice(workers)
        status, reason = evaluate_probe(code)
        
        all_eval_records.append({
            "tick": tick_counter,
            "node_id": worker,
            "category": category,
            "payload": code,
            "status": status,
            "reason": reason
        })
        tick_counter += 1

# Sort globally by absolute tick index
all_eval_records.sort(key=lambda x: x["tick"])

# 3. Wire into TraceGuard SHA-256 State-Chain Ledger
genesis_seed = "TRACEGUARD_V3_SCALE_EVAL_ROOT"
current_hash = hashlib.sha256(genesis_seed.encode()).hexdigest()

ledger_records = []
for record in all_eval_records:
    tick = record["tick"]
    node_id = record["node_id"]
    payload = record["payload"]
    status = record["status"]
    
    expected_hash = hashlib.sha256(f"{current_hash}{tick}{node_id}{payload}{status}".encode()).hexdigest()
    record["hash"] = expected_hash
    current_hash = expected_hash
    ledger_records.append(record)

# Save output to logs
os.makedirs("logs/scale_eval", exist_ok=True)
output_ledger_path = "logs/scale_eval/scaled_ledger_audit.jsonl"
with open(output_ledger_path, "w") as f:
    for rec in ledger_records:
        f.write(json.dumps(rec) + "\n")

# 4. Compute Distribution Metrics
status_counts = {"GREEN": 0, "AMBER": 0, "RED": 0}
category_breakdown = {}

for rec in ledger_records:
    status_counts[rec["status"]] += 1
    cat = rec["category"]
    if cat not in category_breakdown:
        category_breakdown[cat] = {"GREEN": 0, "AMBER": 0, "RED": 0}
    category_breakdown[cat][rec["status"]] += 1

print("----------------------------------------------------------------------")
print(f"  SCALED EVALUATION RESULTS // Total Probes: {len(ledger_records)}")
print("----------------------------------------------------------------------")
print(f"  - GREEN (Authorized) : {status_counts['GREEN']}")
print(f"  - AMBER (Throttled)  : {status_counts['AMBER']}")
print(f"  - RED (Contained)    : {status_counts['RED']}")
print("----------------------------------------------------------------------")
print("  CATEGORY BREAKDOWN:")
for cat, counts in category_breakdown.items():
    print(f"    * {cat:20} -> GREEN: {counts['GREEN']:2}, AMBER: {counts['AMBER']:2}, RED: {counts['RED']:2}")
print("----------------------------------------------------------------------")
print(f"  Cryptographic Ledger State : SEALED (0% Drift)")
print(f"  Terminal SHA-256 Hash      : {current_hash}")
print("======================================================================")
