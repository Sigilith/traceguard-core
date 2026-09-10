class TraceGuard:
    """Zero-trust runtime boundary enforcement engine for autonomous AI agents."""
    
    def __init__(self, allowed_actions: list[str]):
        self.allowed_actions = set(allowed_actions)
        self.breaches = []

    def evaluate_action(self, action: str) -> str:
        if not action or action not in self.allowed_actions:
            self.breaches.append(action)
            return "BLOCK"
        return "ALLOW"

    def get_breach_count(self) -> int:
        return len(self.breaches)
