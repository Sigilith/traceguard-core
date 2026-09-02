import unittest
import os
from three_lineage.core.vault import PrivateAssuranceVault

class TestPrivateAssuranceVault(unittest.TestCase):
    def setUp(self):
        self.vault_path = "test_vault.dat"
        self.vault = PrivateAssuranceVault(vault_path=self.vault_path)

    def tearDown(self):
        if os.path.exists(self.vault_path):
            os.remove(self.vault_path)

    def test_commit_breach_forensics(self):
        success = self.vault.commit_breach_forensics(
            audit_uuid="test-uuid-123",
            risk_score=0.95,
            telemetry={"trigger": "anomaly"}
        )
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.vault_path))
        
        # Verify file content is encrypted (plaintext uuid should not be visible)
        with open(self.vault_path, "rb") as f:
            content = f.read()
        self.assertNotIn(b"test-uuid-123", content)

if __name__ == "__main__":
    unittest.main()
