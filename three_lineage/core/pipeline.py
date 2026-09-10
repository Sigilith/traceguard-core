# THREE-LINEAGE CORE PIPELINE
from three_lineage.aximos.governance import GovernanceEngine

class ThreeLineagePipeline:
    def __init__(self):
        self.gov = GovernanceEngine(fail_closed=True)

    def execute(self, payload):
        decision = self.gov.evaluate(payload)
        if decision["decision"] != "ALLOW" or decision.get("allow_fallback", False):
            raise PermissionError("PIPELINE HALTED: Fail-closed governance invariant triggered.")
        return "EXECUTION_SUCCESS"
