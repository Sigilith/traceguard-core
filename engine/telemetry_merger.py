import json
import hashlib
import glob
import os

def merge_and_verify_streams(log_directory: str, output_path: str):
    """Merges multiple node telemetry JSONL files into a single chronological ledger."""
    all_records = []
    
    # Collect all JSONL streams
    pattern = os.path.join(log_directory, "*.jsonl")
    for file_path in glob.glob(pattern):
        with open(file_path, "r") as f:
            for line in f:
                if line.strip():
                    all_records.append(json.loads(line))
                    
    # Sort globally by tick index
    all_records.sort(key=lambda x: x.get("tick", 0))
    
    # Re-chain and write unified ledger
    genesis_seed = "TRACEGUARD_V3_EXPANDED"
    current_hash = hashlib.sha256(genesis_seed.encode()).hexdigest()
    
    merged_records = []
    for record in all_records:
        tick = record.get("tick")
        node_id = record.get("node_id", "orchestrator_default")
        payload = record.get("payload", record.get("payload_snippet", ""))
        
        # Compute unified global hash incorporating node_id
        expected_hash = hashlib.sha256(f"{current_hash}{tick}{node_id}{payload}".encode()).hexdigest()
        record["hash"] = expected_hash
        current_hash = expected_hash
        merged_records.append(record)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as out:
        for rec in merged_records:
            out.write(json.dumps(rec) + "\n")
            
    print(f"[+] Successfully merged {len(merged_records)} vectors across nodes into: {output_path}")
    print(f"[+] Unified Terminal Hash: {current_hash}")

if __name__ == "__main__":
    merge_and_verify_streams("logs/telemetry", "logs/telemetry/unified_global_ledger.jsonl")
