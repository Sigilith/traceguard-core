import pytest
import asyncio
from traceguard.asyncledger import AsyncEvidenceLedger

@pytest.mark.asyncio
async def test_async_ledger_basic():
    ledger = AsyncEvidenceLedger()
    entry1 = await ledger.append_entry({"action": "test_1", "decision": "ALLOW"})
    entry2 = await ledger.append_entry({"action": "test_2", "decision": "BLOCK"})
    
    assert len(ledger.chain) == 2
    assert entry2["prev_hash"] == entry1["current_hash"]
    assert await ledger.verify_integrity() is True

@pytest.mark.asyncio
async def test_async_concurrency():
    ledger = AsyncEvidenceLedger()
    
    async def simulate_agent_action(i):
        return await ledger.append_entry({"action": f"action_{i}", "decision": "ALLOW"})

    await asyncio.gather(*(simulate_agent_action(i) for i in range(25)))
    assert len(ledger.chain) == 25
    assert await ledger.verify_integrity() is True

@pytest.mark.asyncio
async def test_tamper_detection():
    ledger = AsyncEvidenceLedger()
    await ledger.append_entry({"action": "safe", "decision": "ALLOW"})
    await ledger.append_entry({"action": "unsafe", "decision": "BLOCK"})
    
    # Corrupt a past record manually
    ledger.chain[0]["payload"]["action"] = "tampered_action"
    
    assert await ledger.verify_integrity() is False
