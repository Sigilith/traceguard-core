import unittest
from three_lineage.aximos.governance import LineageGovernanceAdapter

class TestLineageGovernanceAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = LineageGovernanceAdapter()

    def test_govern_telemetry_allowed(self):
        result = self.adapter.govern_telemetry(1.0)
        self.assertEqual(result["decision"], "allow")
        self.assertEqual(result["policy_id"], "P-00")
        self.assertTrue(result["release_response"])

if __name__ == "__main__":
    unittest.main()
