# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import os
import json
import time
from datetime import datetime, timezone

class PredictiveStabilityEngine:
    def __init__(self):
        self.telemetry_dir = ".lineage/telemetry"
        os.makedirs(self.telemetry_dir, exist_ok=True)
        self.stability_log = os.path.join(self.telemetry_dir, "stability_index.jsonl")

    def compute_stability_index(self, heartbeat_jitter_ms: float, socket_probe_count: int, ast_latency_ms: float) -> float:
        print("====================================================")
        print("🔮 PREDICTIVE STABILITY INDEX (PSI) ENGINE")
        print("====================================================")
        print(f"[*] Input Metrics -> Jitter: {heartbeat_jitter_ms}ms | Probes: {socket_probe_count} | AST Latency: {ast_latency_ms}ms")
        
        # Base coefficient weighting
        jitter_penalty = min(heartbeat_jitter_ms / 100.0, 0.4)
        probe_penalty = min(socket_probe_count * 0.05, 0.3)
        latency_penalty = min(ast_latency_ms / 200.0, 0.3)
        
        psi_score = max(0.0, 1.0 - (jitter_penalty + probe_penalty + latency_penalty))
        psi_score = round(psi_score, 4)
        
        print(f"[*] Computed Stability Coefficient (PSI): {psi_score}")
        
        # Pre-emptive throttling determination
        if psi_score >= 0.8:
            status = "NOMINAL (Full Execution Pipeline)"
        elif psi_score >= 0.5:
            status = "WARNING (Pre-emptive Sandbox Throttling Engaged)"
        else:
            status = "CRITICAL DRIFT (Pre-emptive Hard-Kill / Quarantine Imminent)"
            
        print(f"[*] Pre-emptive Action Profile: {status}")
        
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "psi_score": psi_score,
            "status": status,
            "metrics": {
                "jitter_ms": heartbeat_jitter_ms,
                "socket_probes": socket_probe_count,
                "ast_latency_ms": ast_latency_ms
            }
        }
        
        with open(self.stability_log, "a") as f:
            f.write(json.dumps(record) + "\n")
            
        print("[+] Stability index state recorded to telemetry vault.")
        print("====================================================")
        return psi_score

if __name__ == "__main__":
    engine = PredictiveStabilityEngine()
    # Simulate a clean system state with minimal jitter and zero threat vectors
    engine.compute_stability_index(heartbeat_jitter_ms=4.2, socket_probe_count=0, ast_latency_ms=12.5)
