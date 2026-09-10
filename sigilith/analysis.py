import math

def evaluate_structural_regime(telemetry_vector: list, baseline_hash: str, risk_threshold: float = 2.5) -> bool:
    if not telemetry_vector:
        return False
        
    magnitude = math.sqrt(sum(v**2 for v in telemetry_vector))
    max_allowed = math.sqrt(len(telemetry_vector) * (risk_threshold**2))
    
    if magnitude >= max_allowed:
        return False
        
    variance = max(telemetry_vector) - min(telemetry_vector)
    if variance == 0.0 and max(telemetry_vector) > 0.1:
        return False
        
    return True
