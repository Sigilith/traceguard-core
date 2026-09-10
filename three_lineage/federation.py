import json
import os
import time

class Federation:
    def __init__(self):
        self.ledger_dir = "drift_ledger"
        os.makedirs(self.ledger_dir, exist_ok=True)

        self.peer_alerts_file = os.path.join(self.ledger_dir, "peer_alerts.json")
        self.hardening_file = os.path.join(self.ledger_dir, "hardening_events.json")

        # Ensure files exist
        for f in [self.peer_alerts_file, self.hardening_file]:
            if not os.path.exists(f):
                with open(f, "w") as fp:
                    json.dump([], fp)

    def load_local_fingerprint(self):
        return {
            "fingerprint_id": f"fp_{int(time.time())}",
            "drift_hash": hex(hash(time.time()))[:18]
        }

    def load_peer_alerts(self):
        try:
            with open(self.peer_alerts_file, "r") as fp:
                return json.load(fp)
        except:
            return []

    def load_hardening_events(self):
        try:
            with open(self.hardening_file, "r") as fp:
                return json.load(fp)
        except:
            return []

