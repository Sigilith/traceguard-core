import os
import json
import time
from cryptography.fernet import Fernet

class PrivateAssuranceVault:
    def __init__(self, vault_path: str = "vault.dat", secret_key: bytes = None):
        self.vault_path = vault_path
        self.secret_key = secret_key or Fernet.generate_key()
        self.cipher = Fernet(self.secret_key)

    def commit_breach_forensics(self, audit_uuid: str, risk_score: float, telemetry: dict) -> bool:
        """
        Cryptographically seals and locks the forensic record locally.
        Executed in microseconds right before a fail-closed system termination.
        """
        payload = {
            "audit_uuid": audit_uuid,
            "risk_score": risk_score,
            "timestamp_epoch": time.time(),
            "telemetry_data": telemetry
        }
        
        try:
            serialized_data = json.dumps(payload).encode('utf-8')
            encrypted_blob = self.cipher.encrypt(serialized_data)
            
            parent_dir = os.path.dirname(os.path.abspath(self.vault_path))
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
                
            with open(self.vault_path, "ab") as vault_file:
                vault_file.write(encrypted_blob + b"\n")
            return True
        except Exception:
            return False
