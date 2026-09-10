from three_lineage.sovereign_loop import SovereignLoop
from three_lineage.federation import Federation

def print_section(title):
    print(f"\n=== {title} ===")

def render_federation_section():
    fed = Federation()
    peer_alerts = fed.load_peer_alerts()
    local_fp = fed.load_local_fingerprint()
    hardened = fed.load_hardening_events()

    print(f"Local Fingerprint : {local_fp['fingerprint_id']}")
    print(f"Local Drift Hash  : {local_fp['drift_hash']}")

    print("\nPeer Alerts:")
    if not peer_alerts:
        print("- None")
    else:
        for alert in peer_alerts:
            print(f"- Peer {alert.get('peer_id')} reports {alert.get('agent')} as {alert.get('drift_state')} (score={alert.get('drift_score')})")

    print("\nHardening Events:")
    if not hardened:
        print("- None")
    else:
        for event in hardened:
            print(f"- {event['timestamp']} :: boundaries tightened for {event['agent']}")

def dashboard_cycle():
    loop = SovereignLoop(".")
    result = loop.cycle()

    print_section("SIGILITH STRUCTURAL OBSERVATION")
    sig = result.get("sigilith_raw", {})
    print(sig)

    print_section("TRACEGUARD BOUNDARY EVENTS")
    for evt in result.get("traceguard_boundary", {}).get("boundary_events", [])[:10]:
        print(f"- {evt['file']} | {evt['boundary_signal']} | {evt['status']}")

    print_section("TRACEGUARD ENFORCEMENT DECISIONS")
    for dec in result.get("traceguard_kernel", {}).get("enforcement_decisions", [])[:10]:
        print(f"- {dec['file']} | {dec['decision']}")

    print_section("AXIOMOS RISK CLASSIFICATION")
    ax = result.get("axiomos_risk", {})
    print(f"Risk Level: {ax.get('risk_level')}")

    print_section("AXIOMOS RAW LOGS (first 10)")
    for log in ax.get("raw_logs", [])[:10]:
        print(f"- {log['file']} | {log['decision']}")

    print_section("DEREK EXECUTION DECISION")
    decision = result.get("derek_decision", {})
    print(f"Status: {decision.get('status')}")
    print(f"Action: {decision.get('action')}")
    print(f"Message: {decision.get('message')}")
    print(f"Staging Task ID: {decision.get('task_id')}")

    print_section("FEDERATION NETWORK INTELLIGENCE")
    render_federation_section()

    print("\n=== SOVEREIGN DASHBOARD COMPLETE ===\n")

if __name__ == "__main__":
    dashboard_cycle()
