import json
f = open('submission_bundle/protocol_spec.json')
spec = json.load(f)
f.close()
spec['telemetry_schema']['node_id'] = 'string'
b = 'H_n = SHA256(prev || tick || node_id || code)'
spec['ledger_spec']['block_structure'] = b
spec['capabilities']['telemetry'].append('multi_node')
with open('submission_bundle/protocol_spec.json', 'w') as f:
    json.dump(spec, f, indent=2)
readme = '# TraceGuard V3: ControlArena Protocol
'
readme += 'Supports distributed multi-node execution.
'
with open('submission_bundle/README.md', 'w') as f:
    f.write(readme)
print('[+] Multi-node schema and README generated.')
