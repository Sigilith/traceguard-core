# DEREK EXECUTION GATE (NONCE & TIME-BOUND HARDENED)
import time
import hashlib

class DerekExecutionGate:
    def __init__(self, secret_key="traceguard_secure_key"):
        self.secret_key = secret_key

    def dispatch(self, authorization_token, payload):
        if not authorization_token or not authorization_token.startswith("SIGILITH-CRYPTOGRAPHIC-"):
            return "DENY_UNAUTHORIZED_GATE"
            
        parts = authorization_token.split("-")
        if len(parts) != 4:
            return "DENY_MALFORMED_TOKEN"
            
        _, _, timestamp_str, provided_hash = parts
        
        try:
            timestamp = float(timestamp_str)
        except ValueError:
            return "DENY_INVALID_TIMESTAMP"
            
        if time.time() - timestamp > 5:
            return "DENY_TOKEN_EXPIRED"
            
        expected_hash = hashlib.sha256(f"{timestamp}{self.secret_key}".encode()).hexdigest()
        if provided_hash != expected_hash:
            return "DENY_SIGNATURE_MISMATCH"
            
        return "DISPATCH_AUTHORIZED"
