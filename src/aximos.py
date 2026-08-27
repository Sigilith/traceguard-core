class AXIOMOSEvaluator:
    def __init__(self, block_threshold: int = 2):
        self.block_threshold = block_threshold

    def evaluate_logs(self, logs: list) -> str:
        block_count = sum(1 for log in logs if log.get("decision") == "BLOCK")
        if block_count >= self.block_threshold:
            return "HIGH_RISK"
        return "LOW_RISK"
