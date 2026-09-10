def render_federation_section():
    from three_lineage.federation import Federation

    fed = Federation()
    peer_alerts = fed.load_peer_alerts()
    local_fp = fed.load_local_fingerprint()

    print("\n=== FEDERATION ===")
    print(f"Local Fingerprint : {local_fp.get('fingerprint_id')}")
    print(f"Local Drift Hash  : {local_fp.get('drift_hash')}")

    if not peer_alerts:
        print("Peer Alerts       : None")
        return

    print("Peer Alerts       :")
    for alert in peer_alerts:
        agent = alert.get("agent")
        score = alert.get("drift_score")
        state = alert.get("drift_state")
        peer = alert.get("peer_id")

        print(f" - Peer {peer} reports {agent} as {state} (score={score})")

    hardened = fed.load_hardening_events()
    if hardened:
        print("\nHardening Events  :")
        for event in hardened:
            print(f" - {event['timestamp']} :: boundaries tightened for {event['agent']}")
