import time
from three_lineage.sovereign_loop import SovereignLoop
from three_lineage.sovereign_dashboard import dashboard_cycle

def heartbeat(delay=5):
    loop = SovereignLoop(".")
    while True:
        print("\n=== SOVEREIGN HEARTBEAT CYCLE START ===")
        dashboard_cycle()
        print("=== SOVEREIGN HEARTBEAT CYCLE END ===\n")
        time.sleep(delay)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        heartbeat()
    else:
        delay = int(sys.argv[1])
        heartbeat(delay)
