import os
import json
import hashlib
import time

print("======================================================================")
print("  TRACEGUARD V3 // MULTI-NODE DISTRIBUTED ARENA STRESS-TEST ENGINE")
print("======================================================================")

# 1. Initialize Simulated Node Streams
nodes = ["agent_planner_01", "agent_coder_02", "agent_executor_03"]
os.makedirs("logs/cluster_telemetry", exist_ok=True)

# Simulate asynchronous telemetry generation across 3 nodes
raw_events = [
    {"tick": 101, "node_id": "agent_planner_01", "payload": "import math; math.sqrt(25)", "status": "GREEN"},
    {"tick": 102, "node_id": "agent_coder_02", "payload": "for i in range(1000): pass", "status": "AMBER"},
    {"tick": 103, "node_id": "agent_executor_03", "payload": "import pickle; pickle.loads(bad_data)", "status": "RED"},
    {"tick": 104, "node_id": "agent_planner_01", "payload": "os.system('rm -rf /')", "status": "RED"},
    {"tick": 105, "node_id": "agent_coder_02", "payload": "print('Safe output')", "status": "GREEN"},
]

# Write node-local logs
for node in nodes:
    node_records = [e for e in raw_events if e["node_id"] == node]
    path = f"logs/cluster_telemetry/{node}.jsonl"
    with open(path, "w") as f:
        for rec in node_records:
            f.write(json.dumps(rec) + "\n")

print("[+] Node-local telemetry streams initialized.")

# 2. Global Telemetry Merger & Hash-Chain Composition
all_records = []
for node in nodes:
    path = f"logs/cluster_telemetry/{node}.jsonl"
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    all_records.append(json.loads(line))

# Sort globally by absolute tick index
all_records.sort(key=lambda x: x["tick"])

genesis_seed = "TRACEGUARD_V3_CLUSTER_ROOT"
current_hash = hashlib.sha256(genesis_seed.encode()).hexdigest()

unified_ledger = []
for record in all_records:
    tick = record["tick"]
    node_id = record["node_id"]
    payload = record["payload"]
    
    # Compute global Merkle-style state chain hash
    expected_hash = hashlib.sha256(f"{current_hash}{tick}{node_id}{payload}".encode()).hexdigest()
    record["global_hash"] = expected_hash
    current_hash = expected_hash
    unified_ledger.append(record)

print(f"[+] Merged {len(unified_ledger)} cluster events into unified global ledger.")
print(f"[+] Terminal Global State Hash: {current_hash[:16]}...")

# 3. Cross-Node Collapse Detection & Arena Health Check
window_size = 3
red_events = [r for r in unified_ledger if r["status"] == "RED"]
global_collapse_triggered = False

for idx, event in enumerate(red_events):
    cluster_count = 1
    current_tick = event["tick"]
    for subsequent in red_events[idx+1:]:
        if subsequent["tick"] - current_tick <= window_size:
            cluster_count += 1
    if cluster_count >= 2:
        global_collapse_triggered = True
        break

print("----------------------------------------------------------------------")
print("  ARENA STRESS-TEST EVALUATION RESULTS:")
print(f"  - Total Cluster Red Events : {len(red_events)}")
print(f"  - Temporal Window ($\Delta t$) : {window_size} ticks")
print(f"  - Global Governance State  : {'CLUSTER_COLLAPSE_FREEZE' if global_collapse_triggered else 'STABLE_FEDERATED'}")
print("======================================================================")
