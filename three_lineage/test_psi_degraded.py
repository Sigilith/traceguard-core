# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
from three_lineage.predictive_stability import PredictiveStabilityEngine

engine = PredictiveStabilityEngine()

print("\n--- SCENARIO A: NOMINAL BASELINE ---")
engine.compute_stability_index(heartbeat_jitter_ms=3.5, socket_probe_count=0, ast_latency_ms=10.0)

print("\n--- SCENARIO B: DEGRADED DRIFT & SOCKET PROBES ---")
engine.compute_stability_index(heartbeat_jitter_ms=65.0, socket_probe_count=3, ast_latency_ms=140.0)

print("\n--- SCENARIO C: CRITICAL HARD-KILL THRESHOLD ---")
engine.compute_stability_index(heartbeat_jitter_ms=120.0, socket_probe_count=8, ast_latency_ms=350.0)
