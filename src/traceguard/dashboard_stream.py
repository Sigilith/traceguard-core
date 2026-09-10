import asyncio
from traceguard.aximos import AXIOMOSEvaluator
from traceguard.asyncledger import AsyncEvidenceLedger

class DashboardStreamer:
    """Streams live AXIOMOS risk telemetry and ledger hash chain states for enterprise dashboards."""
    
    def __init__(self, block_threshold: int = 2):
        self.evaluator = AXIOMOSEvaluator(block_threshold=block_threshold)
        self.ledger = AsyncEvidenceLedger()

    async def stream_telemetry(self):
        """Asynchronous generator yielding real-time risk indicators and cryptographic proofs."""
        while True:
            risk_status = self.evaluator.evaluate_logs(self.ledger.chain)
            head_hash = self.ledger.chain[-1]["current_hash"] if self.ledger.chain else "0" * 64
            
            yield {
                "status": "SECURE_PERIMETER_ACTIVE",
                "chain_length": len(self.ledger.chain),
                "axiomos_risk": risk_status,
                "head_hash": head_hash
            }
            await asyncio.sleep(1.0)
