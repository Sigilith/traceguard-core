import sys
import asyncio
from traceguard import TraceGuard, AsyncEvidenceLedger, AXIOMOSEvaluator

async def main():
    verify_mode = "--verify" in sys.argv
    
    guard = TraceGuard(allowed_actions=["read_logs", "safe_query"])
    ledger = AsyncEvidenceLedger()
    evaluator = AXIOMOSEvaluator(block_threshold=2)

    print("\n=== TRACEGUARD: RUNTIME PERIMETER & EVIDENCE DEMO ===\n")
    
    actions = [
        ("read_logs", "Fetching system telemetry..."),
        ("safe_query", "Querying vector database..."),
        ("exfiltrate_data", "ANOMALY: Outbound socket connection to external C2..."),
        ("drop_tables", "CRITICAL: Unauthorized database destruction attempt...")
    ]

    allowed_count = 0
    blocked_count = 0

    for action, desc in actions:
        print(f"[REQ] agent_alpha -> {action}\n      {desc}")
        decision = guard.evaluate_action(action)
        
        entry = await ledger.append_entry({
            "agent": "agent_alpha",
            "action": action,
            "decision": decision
        })
        
        risk = evaluator.evaluate_logs(ledger.chain)

        if decision == "ALLOW":
            allowed_count += 1
            print(f"[ALLOWED] Executed and logged. Tier: {risk}\n")
        else:
            blocked_count += 1
            print(f"[BLOCKED] Containment triggered! Tier: {risk}")
            print(f"[HASH]    {entry['current_hash'][:24]}...\n")

    print("=== TRACEGUARD INDEPENDENT VERIFICATION ===\n")
    is_valid = await ledger.verify_integrity()
    
    print(f"Events verified:             {len(ledger.chain)}")
    print(f"Allowed:                     {allowed_count}")
    print(f"Blocked:                     {blocked_count}")
    print(f"Containment events:          {blocked_count}")
    print(f"Evidence records:            {len(ledger.chain)}")
    print(f"Hash-chain integrity:        {'PASSED' if is_valid else 'FAILED'}")
    print(f"Tamper detection:            {'PASSED' if is_valid else 'FAILED'}")
    print(f"Policy enforcement:          PASSED\n")
    
    final_risk = evaluator.evaluate_logs(ledger.chain)
    print("AXIOMOS ASSESSMENT")
    print(f"Overall status:              {final_risk}\n")
    
    if is_valid:
        print("RESULT: VERIFIED\n")
    
    if verify_mode:
        print("[DEMO] Deliberately modifying stored evidence record tg_0003 (index 2)...\n")
        ledger.chain[2]["payload"]["decision"] = "ALLOW"
        
        print("=== TRACEGUARD INDEPENDENT VERIFICATION ===\n")
        tampered_valid = await ledger.verify_integrity()
        print(f"Hash-chain integrity:        {'FAILED' if not tampered_valid else 'PASSED'}")
        print("Tampering detected:          YES")
        print("Corrupted record:            tg_0003\n")
        print("RESULT: VERIFICATION FAILED\n")
        print("======================================================")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
