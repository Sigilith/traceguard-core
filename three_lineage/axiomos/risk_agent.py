# RISK CLASSIFICATION AGENT (ADVANCED SLIDING-WINDOW HARDENED)
from collections import deque

class RiskAgent:
    def __init__(self, window_size=3):
        self.window_size = window_size
        self.telemetry_history = deque(maxlen=window_size)

    def classify_risk(self, telemetry_stream):
        current_score = telemetry_stream.get("drift_score", 0.0)
        self.telemetry_history.append(current_score)
        
        rolling_avg = sum(self.telemetry_history) / len(self.telemetry_history)
        
        if rolling_avg >= 3.0:
            return "HIGH_RISK"
        elif rolling_avg >= 1.5:
            return "MEDIUM_RISK"
        return "LOW_RISK"
