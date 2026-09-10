import pytest
import asyncio
from traceguard import AsyncEvidenceLedger

@pytest.mark.asyncio
async def test_ledger_integrity_valid():
    ledger = AsyncEvidenceLedger()
    await ledger.append_entry({"action": "test_1"})
    await ledger.append_entry({"action": "test_2"})
    assert await ledger.verify_integrity() is True

@pytest.mark.asyncio
async def test_ledger_tamper_detection():
    ledger = AsyncEvidenceLedger()
    await ledger.append_entry({"action": "test_1"})
    await ledger.append_entry({"action": "test_2"})
    
    # Tamper with historical payload
    ledger.chain[0]["payload"]["action"] = "tampered"
    assert await ledger.verify_integrity() is False
