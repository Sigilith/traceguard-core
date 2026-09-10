import os
import glob
import hashlib
import json
import time
import pandas as pd

print("==================================================")
print(" THREE-LINEAGE NASA BATTERY TELEMETRY INGESTION")
print("==================================================")

data_dir = "./nasa_battery_data"
receipt_dir = ".lineage/derek_receipts"
os.makedirs(receipt_dir, exist_ok=True)

csv_files = glob.glob(os.path.join(data_dir, "**", "*.csv"), recursive=True)
print(f"[*] Discovered {len(csv_files)} NASA telemetry CSV files.")

ingestion_records = []
for file_path in csv_files[:5]:
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    try:
        df = pd.read_csv(file_path)
        row_count = len(df)
        status = "INGESTED_VALID"
    except Exception as e:
        row_count = 0
        status = f"PARSE_ERROR: {e}"

    record = {
        "file": file_path,
        "sha256": file_hash,
        "rows": row_count,
        "status": status,
        "timestamp": time.time()
    }
    ingestion_records.append(record)
    print(f"    -> Ingested: {os.path.basename(file_path)} | Rows: {row_count} | Status: {status}")

receipt = {
    "pipeline": "ThreeLineage NASA Battery Telemetry Ingestion",
    "timestamp_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    "total_files_processed": len(ingestion_records),
    "records": ingestion_records
}

receipt_path = os.path.join(receipt_dir, f"nasa_ingestion_{int(time.time())}.json")
with open(receipt_path, "w") as f:
    json.dump(receipt, f, indent=2)

print(f"[+] Cryptographic ingestion receipt sealed at: {receipt_path}")
print("==================================================")
print(" INGESTION PIPELINE EXECUTION COMPLETE.")
print("==================================================")
