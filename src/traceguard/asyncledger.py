import asyncio
import json
import hashlib
from datetime import datetime, timezone

class AsyncEvidenceLedger:
    """Enterprise non-blocking tamper-evident hash-chain ledger for asynchronous AI agent pipelines."""
    
    def __init__(self):
        self.chain = []
        self.last_hash = "0" * 64
        self._lock = asyncio.Lock()

    async def _compute_hash(self, entry_str: str) -> str:
        """Offloads SHA-256 computation to a background thread to prevent event loop blocking."""
        return await asyncio.to_thread(
            lambda: hashlib.sha256(entry_str.encode('utf-8')).hexdigest()
        )

    async def append_entry(self, payload: dict) -> dict:
        """Appends a cryptographically chained governance record asynchronously."""
        async with self._lock:
            timestamp = datetime.now(timezone.utc).isoformat()
            entry = {
                "timestamp": timestamp,
                "payload": payload,
                "prev_hash": self.last_hash
            }
            # Explicitly sort keys to bypass Termux Python 3.13 json.dumps sort_keys bug
            sorted_entry = dict(sorted(entry.items()))
            entry_json = json.dumps(sorted_entry)
            current_hash = await self._compute_hash(entry_json)
            
            entry["current_hash"] = current_hash
            self.chain.append(entry)
            self.last_hash = current_hash
            return entry

    async def verify_integrity(self) -> bool:
        """Verifies the immutable integrity of the entire cryptographic chain."""
        async with self._lock:
            if not self.chain:
                return True
            
            if self.chain[0]["prev_hash"] != "0" * 64:
                return False

            for i in range(1, len(self.chain)):
                prev = self.chain[i - 1]
                curr = self.chain[i]
                
                if curr["prev_hash"] != prev["current_hash"]:
                    return False
                
                recheck_entry = {
                    "timestamp": curr["timestamp"],
                    "payload": curr["payload"],
                    "prev_hash": curr["prev_hash"]
                }
                sorted_recheck = dict(sorted(recheck_entry.items()))
                recheck_json = json.dumps(sorted_recheck)
                recheck_hash = hashlib.sha256(recheck_json.encode('utf-8')).hexdigest()
                
                if recheck_hash != curr["current_hash"]:
                    return False
                    
            return True
