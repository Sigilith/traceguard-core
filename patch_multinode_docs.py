import json
import os

# 1. Update the Protocol Spec for Multi-Node
with open('submission_bundle/protocol_spec.json', 'r') as f:
    spec = json.load(f)

spec['telemetry_schema']['node_id'] = "string (e.g., 'agent_planner_01')"
spec['ledger_spec']['block_structure'] = "H_n = SHA256(H_{n-1} || tick || 
node_id || full_payload_code)"
spec['capabilities']['telemetry'].append("multi_node_interleaving")

with open('submission_bundle/protocol_spec.json', 'w') as f:
    json.dump(spec, f, indent=2)

# 2. Generate the Formal README Documentation
readme_content = """# TraceGuard V3: ControlArena Protocol

TraceGuard is a deterministic AST-based multi-phase command-gating 
runtime. It evaluates raw execution payloads, returning a governance state 
(GREEN, AMBER, RED, SYNTAX) alongside a cryptographically linked SHA-256 
telemetry ledger.

## Multi-Node Execution
The protocol supports distributed agent execution. Pass `node_id` in the 
gating request to interleave multiple agent streams into a single unbroken 
ledger.

## Usage
```python
from controlarena_submission_wrapper import gate_command

payload = {
    "node_id": "orchestrator_01",
    "code": "import math\\nmath.sqrt(16)"
}
result = gate_command(payload)
