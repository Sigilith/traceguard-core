from traceguard.evidence import EvidenceLedger

ledger = EvidenceLedger()
ledger.record({"event": "ALLOW"})
ledger.record({"event": "BLOCK"})
print("Ledger verified:", ledger.verify_chain())
