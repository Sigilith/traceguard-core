import unittest
from three_lineage.aximos.governance import LineageGovernanceAdapter

class TestEventHandlerBridge(unittest.TestCase):
    def setUp(self):
        self.governance = LineageGovernanceAdapter()

    def test_evaluate_event_types(self):
        for event in ['safe', 'suspicious', 'breach', 'quarantine', 'shutdown']:
            result = self.governance.evaluate(event, {"agent_id": "agent-001", "component": "core"})
            self.assertIn("decision", result)
            self.assertIn("policy_id", result)

if __name__ == "__main__":
    unittest.main()
