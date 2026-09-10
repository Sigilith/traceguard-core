import hashlib
import hmac

TRACEGUARD_SECRET = b"sigilith_epoch_2026"

def generate_bound_nonce(anchor_hash: str) -> str:
    return hmac.new(TRACEGUARD_SECRET, anchor_hash.encode(), hashlib.sha256).hexdigest()

def verify_nonce_binding(current_nonce: str, anchor_hash: str) -> bool:
    if not current_nonce or not anchor_hash:
        return False
    expected = generate_bound_nonce(anchor_hash)
    return hmac.compare_digest(current_nonce, expected)
