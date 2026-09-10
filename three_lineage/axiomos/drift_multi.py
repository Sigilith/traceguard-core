from three_lineage.axiomos.driftsentinel import DriftSentinel

class MultiAgentDrift:
    """
    Multi-agent drift controller for the Sovereign Gauntlet.
    Tracks drift for SIGILITH, TRACEGUARD, AXIOMOS, DEREK, and any external agents.
    """

    def __init__(self):
        self.sentinel = DriftSentinel()
        self.agents = [
            "SIGILITH_SENSOR",
            "TRACEGUARD_ENFORCER",
            "AXIOMOS_PIPELINE",
            "DEREK_GATE"
        ]

    def log_cycle(self, cycle_result):
        """
        Logs drift telemetry for all agents based on SovereignLoop cycle output.
        """
        # SIGILITH
        sig = cycle_result.get("sigilith_scan", {})
        self.sentinel.log_behavior(
            agent="SIGILITH_SENSOR",
            risk_level=sig.get("structure_state", "NORMAL"),
            blocks=sig.get("anomaly_count", 0),
            allows=1,
            files_touched=sig.get("files_scanned", 0)
        )

        # TRACEGUARD
        tg = cycle_result.get("traceguard_map", {})
        self.sentinel.log_behavior(
            agent="TRACEGUARD_ENFORCER",
            risk_level=tg.get("boundary_state", "NORMAL"),
            blocks=tg.get("violations", 0),
            allows=1,
            files_touched=len(tg.get("events", []))
        )

        # AXIOMOS
        ax = cycle_result.get("axiomos_risk", {})
        self.sentinel.log_behavior(
            agent="AXIOMOS_PIPELINE",
            risk_level=ax.get("risk_level", "LOW_RISK"),
            blocks=sum(1 for r in ax.get("raw_logs", []) if r["decision"] == "BLOCK"),
            allows=sum(1 for r in ax.get("raw_logs", []) if r["decision"] == "ALLOW"),
            files_touched=len(ax.get("raw_logs", []))
        )

        # DEREK
        dk = cycle_result.get("derek_gate", {})
        self.sentinel.log_behavior(
            agent="DEREK_GATE",
            risk_level=dk.get("decision", "ALLOW"),
            blocks=int(dk.get("decision") == "HALT"),
            allows=int(dk.get("decision") == "ALLOW"),
            files_touched=len(ax.get("raw_logs", []))
        )

    def evaluate_all(self):
        """
        Returns drift reports for all agents.
        """
        return {
            agent: self.sentinel.compute_drift(agent)
            for agent in self.agents
        }
