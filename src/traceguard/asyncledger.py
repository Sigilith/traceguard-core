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
            sorted_entry = dict(sorted(entry.items()))
            entry_json = json.dumps(sorted_entry)
            current_hash = await self._compute_hash(entry_json)
            
            entry["current_hash"] = current_hash
            self.chain.append(entry)
            self.last_hash = current_hash
            return entry

    async def verify_integrity(self) -> bool:
        """Verifies immutable chain integrity by recomputing hashes sequentially from genesis."""
        async with self._lock:
            if not self.chain:
                return True
            
            expected_prev_hash = "0" * 64

            for curr in self.chain:
                # 1. Validate previous hash linkage
                if curr["prev_hash"] != expected_prev_hash:
                    return False
                
                # 2. Recompute current block hash from its source data
                recheck_entry = {
                    "timestamp": curr["timestamp"],
                    "payload": curr["payload"],
                    "prev_hash": curr["prev_hash"]
                }
                sorted_recheck = dict(sorted(recheck_entry.items()))
                recheck_json = json.dumps(sorted_recheck)
                recheck_hash = hashlib.sha256(recheck_json.encode('utf-8')).hexdigest()
                
                # 3. Validate stored hash matches recomputed hash
                if recheck_hash != curr["current_hash"]:
                    return False
                
                expected_prev_hash = recheck_hash
                    
            return True
