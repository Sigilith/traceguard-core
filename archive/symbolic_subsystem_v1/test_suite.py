# Copyright (c) 2026 Sigilith-labs / Ky Nash. All rights reserved.
import unittest
import os
import json
from three_lineage_v2 import ThreeLineageEngineV2

class TestThreeLineageEngineV2(unittest.TestCase):
    
    def setUp(self):
        self.engine = ThreeLineageEngineV2()
        self.test_asset_name = "Test Artifact Alpha"
        self.test_signature = "Manual manual variance in glyph rendering"

    def test_dynamic_taxonomy_ingestion(self):
        result = self.engine.dynamic_taxonomy_ingest(
            self.test_asset_name, 
            self.test_signature, 
            "Experimental Symbolic Corpus"
        )
        self.assertEqual(result["name"], self.test_asset_name)
        self.assertEqual(result["ingestion_mode"], "Adaptive-Dynamic")
        self.assertEqual(result["status"], "Verified")

    def test_heuristic_anomaly_sandbox(self):
        asset_data = {
            "name": self.test_asset_name,
            "architecture": self.test_signature,
            "status": "Verified"
        }
        status = self.engine.heuristic_anomaly_sandbox(asset_data)
        self.assertEqual(status, "Aligned-Tolerated")

    def test_probabilistic_psi_scoring(self):
        psi_clean = self.engine.probabilistic_psi_scoring(10, [0.0, 0.0])
        psi_degraded = self.engine.probabilistic_psi_scoring(10, [1.0, 0.5])
        self.assertGreater(psi_clean, psi_degraded)
        self.assertGreaterEqual(psi_clean, 0.0)
        self.assertLessEqual(psi_clean, 1.0)

    def test_manifest_integrity_and_hashing(self):
        self.assertTrue(os.path.exists(self.engine.manifest_path), "Manifest path must exist.")
        with open(self.engine.manifest_path, "r") as f:
            data = json.load(f)
        self.assertIn("artifacts", data)
        for artifact in data["artifacts"]:
            h = self.engine.compute_hash(artifact)
            self.assertEqual(len(h), 16, "Cryptographic hash must be truncated to 16 hex characters.")

if __name__ == "__main__":
    unittest.main()
