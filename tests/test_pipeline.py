import unittest
from three_lineage.core.pipeline import LineagePipeline

class TestLineagePipeline(unittest.TestCase):
    def test_pipeline_dispatch(self):
        pipeline = LineagePipeline()
        result = pipeline.handle_event("suspicious", {"agent_id": "test-agent"})
        self.assertEqual(result["event_type"], "suspicious")
        self.assertIn("governance", result)
        self.assertEqual(result["governance"]["decision"], "allow")

if __name__ == "__main__":
    unittest.main()
