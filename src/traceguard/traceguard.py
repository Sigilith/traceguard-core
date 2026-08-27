import time

class TraceGuard:
    def __init__(self, allowed_actions=None):
        self.allowed_actions = allowed_actions or ["read_logs", "safe_query"]
        self.audit_log = []

    def evaluate_action(self, action: str, context: dict = None) -> str:
        timestamp = time.time()
        context = context or {}
        
        if action in self.allowed_actions:
            decision = "ALLOW"
        else:
            decision = "BLOCK"
            
        log_entry = {
            "timestamp": timestamp,
            "action": action,
            "context": context,
            "decision": decision
        }
        self.audit_log.append(log_entry)
        return decision

    def get_logs(self):
        return self.audit_log
