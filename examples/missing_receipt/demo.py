#!/usr/bin/env python3
"""A real process dies after its side effect, before its completion receipt."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from core.arbitration_engine import SovereignExecutionGate, PostureArbitrationEngine
from core.ledger_writer import AppendOnlyLedgerWriter

ROOT = Path(__file__).resolve().parent


def effect(directory, crash=False):
    """Local append is intentionally non-idempotent so duplicates are visible."""
    with (directory / 'deliveries.txt').open('a') as handle:
        handle.write('DELIVERED\n')
        handle.flush()
        os.fsync(handle.fileno())
    fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    if crash:
        os._exit(77)  # no exception handler, finally block or completion receipt
    return 'delivered'


def worker(directory, mode):
    directory.mkdir(parents=True, exist_ok=True)
    if mode.startswith('unsafe'):
        effect(directory, crash=mode == 'unsafe-crash')
        return {'outcome': 'completed'}
    writer = AppendOnlyLedgerWriter(str(directory / 'ledger.jsonl'))
    gate = SovereignExecutionGate(writer, PostureArbitrationEngine())
    votes = ['BLACK_ABORT'] if mode == 'veto' else ['GREEN_NOMINAL']
    try:
        if mode == 'storage-fault':
            # Inject at the actual persistence boundary; reservation fsync fails.
            with patch('core.ledger_writer.os.fsync', side_effect=OSError('injected fsync failure')):
                gate.execute_governed_action('local-delivery', votes, effect, directory)
        else:
            gate.execute_governed_action('local-delivery', votes, effect, directory, mode == 'crash')
        return {'outcome': 'completed'}
    except Exception as error:
        return {'outcome': 'blocked_or_failed', 'error_type': type(error).__name__, 'detail': str(error)}


def invoke(directory, mode):
    result = subprocess.run([sys.executable, str(ROOT / 'demo.py'), '_worker',
                             '--output', str(directory), '--mode', mode],
                            capture_output=True, text=True, timeout=15)
    if mode in ('crash', 'unsafe-crash'):
        if result.returncode != 77:
            raise RuntimeError(f'Expected crash exit 77, got {result.returncode}: {result.stderr}')
        return {'outcome': 'process_terminated', 'exit_code': 77}
    if result.returncode:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def count(directory):
    file = directory / 'deliveries.txt'
    return len(file.read_text().splitlines()) if file.exists() else 0


def run(output):
    output.mkdir(parents=True, exist_ok=False)  # never mix evidence from runs
    events = []
    for mode in ('normal', 'veto', 'storage-fault', 'crash'):
        directory = output / mode
        result = invoke(directory, mode)
        events.append({'scenario': mode, **result, 'deliveries': count(directory)})
    crash = output / 'crash'
    before = AppendOnlyLedgerWriter(str(crash / 'ledger.jsonl')).scan_integrity()
    events.append({'scenario': 'restart', **invoke(crash, 'normal'), 'deliveries': count(crash)})
    unsafe = output / 'unsafe-retry'
    invoke(unsafe, 'unsafe-crash')
    invoke(unsafe, 'unsafe-retry')
    events.append({'scenario': 'unsafe-retry', 'outcome': 'duplicate', 'deliveries': count(unsafe)})
    after = AppendOnlyLedgerWriter(str(crash / 'ledger.jsonl')).scan_integrity()
    checks = {
        'normal_delivers_once': events[0]['outcome'] == 'completed' and events[0]['deliveries'] == 1,
        'veto_no_effect': events[1].get('error_type') == 'GovernanceDeniedError' and events[1]['deliveries'] == 0,
        'reservation_fault_no_effect': events[2].get('error_type') == 'GovernanceDeniedError' and events[2]['deliveries'] == 0,
        'crash_effect_without_receipt': events[3]['deliveries'] == 1 and len(before.get('unresolved_invocations', [])) == 1,
        'restart_blocks_without_duplicate': events[4].get('error_type') == 'GovernanceDeniedError' and 'Unresolved' in events[4].get('detail', '') and events[4]['deliveries'] == 1,
        'unresolved_persists': before.get('unresolved_invocations') == after.get('unresolved_invocations') and after['status'] == 'VALID',
        'unsafe_retry_duplicates': count(unsafe) == 2,
    }
    evidence = {'claim': 'An unresolved EXECUTION_STARTED blocks subsequent reservations through this gate on the same ledger.',
                'checks': checks, 'events': events, 'crash_ledger_scan': {k: v for k, v in after.items() if not isinstance(v, bytes)},
                'runtime': sys.version, 'platform': sys.platform,
                'core_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'core').glob('*.py')}}
    (output / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
    lines = ['THE ACTION HAPPENED. THE RECEIPT DID NOT.', '']
    lines += [f"{e['scenario']:15} {e['outcome']:20} deliveries={e['deliveries']}" for e in events]
    lines += ['', 'Checks: ' + ('PASS' if all(checks.values()) else 'FAIL'),
              'The unresolved action is preserved. No automatic reconciliation or retry.',
              'Unsafe retry is a deliberately naive comparison, not a benchmark of other products.']
    (output / 'timeline.txt').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    if not all(checks.values()):
        raise RuntimeError('Demonstration did not meet its acceptance checks')
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['run', '_worker'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--mode', default='normal')
    args = parser.parse_args()
    if args.command == '_worker':
        print(json.dumps(worker(args.output.resolve(), args.mode)))
    else:
        run(args.output.resolve())

if __name__ == '__main__':
    main()
