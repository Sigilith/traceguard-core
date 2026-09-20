from traceguard.traceguard import TraceGuard
from traceguard.aximos import AXIOMOSEvaluator
from traceguard.evidence import EvidenceLedger

tg = TraceGuard()
ledger = EvidenceLedger()
ax = AXIOMOSEvaluator(block_threshold=1)

logs = []
logs.append(tg.allow("legitimate_action"))
logs.append(tg.block("unauthorized_action"))
ledger.record(logs[-1])
ledger.verify_chain()
logs.append({"decision": "BLOCK"})  # simulate tamper
risk = ax.evaluate_logs(logs)

print("Zero-Trust Demo Complete")
print("Risk Level:", risk)
