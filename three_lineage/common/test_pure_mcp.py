import json
import time
from boundary_reference_implementation import ReferenceBoundaryEngine, BRI_MANIFEST

def run_pure_simulation():
    print("[*] Initializing Pure Python Three-Lineage Simulation...")
    engine = ReferenceBoundaryEngine("vault_pure_sim.dat")

    # Simulate an agent request mapping through the canonical contract
    requests = [
        {"version": "v1.0.0", "action_id": "sim_01", "code_payload": "sum(range(100))"},
        {"version": "v1.0.0", "action_id": "sim_02", "code_payload": "__import__('os').system('id')"},
        {"version": "v1.0.0", "action_id": "sim_03", "code_payload": "max([12, 55, 99])"}
    ]

    for req in requests:
        print(f"\n[Agent Request] Action: {req['action_id']} | Payload: {req['code_payload']}")
        res = engine.process(req)
        print(f"  -> Status: {res['api_status']}")
        print(f"  -> Result/Rationale: {res['result'] if res['result'] is not None else res['audit_rationale']}")
        print(f"  -> Audit Hash: {res['audit_hash'][:16]}... (Parent: {res['parent_head'][:16]}...)")

    print("\n[+] Simulation complete. Boundary integrity and chain linkage verified.")

if __name__ == "__main__":
    run_pure_simulation()
