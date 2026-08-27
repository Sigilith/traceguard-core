class AssuranceMatrix:
    def calculate_tier(self, consequence: int, autonomy: int, oversight: bool) -> dict:
        score = consequence + autonomy - (2 if oversight else 0)
        if score >= 4:
            tier = "Tier 3 — High Impact"
        elif score >= 2:
            tier = "Tier 2 — Moderate Impact"
        else:
            tier = "Tier 1 — Low Impact"
            
        return {
            "score": score,
            "tier": tier,
            "oversight_enforced": oversight
        }
