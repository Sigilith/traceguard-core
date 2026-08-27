from traceguard.aximos import AXIOMOSEvaluator

ax = AXIOMOSEvaluator(block_threshold=2)
logs = [{"decision": "ALLOW"}, {"decision": "BLOCK"}, {"decision": "BLOCK"}]
print("Drift Risk:", ax.evaluate_logs(logs))
