from pathlib import Path
import json
import time
from statistics import mean

class DriftSentinel:
    """
    Behavioral drift analyzer for the Sovereign Gauntlet.
    Tracks cumulative agent behavior over time and detects
    subtle trajectory shifts that never trip single-event thresholds.
    """

    def __init__(self, ledger_path="drift_ledger/agent_behavior.log"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.window_size = 75  # rolling window of past cycles

    def log_behavior(self, agent, risk_level, blocks, allows, files_touched):
        """
        Append a single behavioral record to the drift ledger.
        """
        entry = {
            "ts": int(time.time()),
            "agent": agent,
            "risk_level": risk_level,
            "blocks": blocks,
            "allows": allows,
            "files_touched": files_touched,
        }
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _load_window(self, agent):
        """
        Load the last N entries for the given agent.
        """
        if not self.ledger_path.exists():
            return []

        lines = self.ledger_path.read_text(encoding="utf-8").splitlines()
        records = [json.loads(line) for line in lines if json.loads(line).get("agent") == agent]
        return records[-self.window_size:]

    def compute_drift(self, agent):
        """
        Compute drift score and classify STABLE / UNSTABLE.
        """
        window = self._load_window(agent)
        if len(window) < 5:
            return {"drift_score": 0.0, "drift_state": "STABLE"}

        # Extract metrics
        blocks = [r["blocks"] for r in window]
        allows = [r["allows"] for r in window]
        files = [r["files_touched"] for r in window]
        risk_levels = [r["risk_level"] for r in window]

        # Baselines
        baseline_blocks = mean(blocks)
        baseline_allows = mean(allows)
        baseline_files = mean(files)
        high_risk_freq = risk_levels.count("HIGH_RISK") / len(risk_levels)

        # Current record
        latest = window[-1]
        delta_blocks = abs(latest["blocks"] - baseline_blocks)
        delta_files = abs(latest["files_touched"] - baseline_files)

        # Drift score (weighted)
        drift_score = (
            (delta_blocks / (baseline_blocks + 1)) * 0.4 +
            (delta_files / (baseline_files + 1)) * 0.3 +
            (high_risk_freq * 0.3)
        )

        drift_state = "UNSTABLE" if drift_score > 0.65 else "STABLE"

        return {
            "drift_score": round(drift_score, 3),
            "drift_state": drift_state,
            "baseline_blocks": round(baseline_blocks, 2),
            "baseline_files": round(baseline_files, 2),
            "high_risk_freq": round(high_risk_freq, 2),
        }
