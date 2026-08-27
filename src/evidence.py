import hashlib
import json

class EvidenceLedger:
    def __init__(self):
        self.chain = []
        self.genesis_hash = "0" * 64

    def append_entry(self, data: dict) -> dict:
        previous_hash = self.chain[-1]["current_hash"] if self.chain else self.genesis_hash
        
        entry = {
            "index": len(self.chain),
            "data": data,
            "previous_hash": previous_hash
        }
        
        encoded_payload = json.dumps(entry, sort_keys=True).encode()
        current_hash = hashlib.sha256(encoded_payload).hexdigest()
        
        entry["current_hash"] = current_hash
        self.chain.append(entry)
        return entry

    def verify_integrity(self) -> bool:
        if not self.chain:
            return True
            
        for i, entry in enumerate(self.chain):
            expected_prev = self.chain[i - 1]["current_hash"] if i > 0 else self.genesis_hash
            if entry["previous_hash"] != expected_prev:
                return False
                
            recheck_entry = entry.copy()
            current_hash = recheck_entry.pop("current_hash")
            encoded_payload = json.dumps(recheck_entry, sort_keys=True).encode()
            if hashlib.sha256(encoded_payload).hexdigest() != current_hash:
                return False
                
        return True

    def tamper_with_entry(self, index: int, malicious_data: dict):
        if 0 <= index < len(self.chain):
            self.chain[index]["data"] = malicious_data
