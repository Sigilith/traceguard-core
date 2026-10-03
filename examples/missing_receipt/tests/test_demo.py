import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from demo import run, effect
from core.ledger_writer import AppendOnlyLedgerWriter
from core.arbitration_engine import SovereignExecutionGate, PostureArbitrationEngine, GovernanceDeniedError, CompletionRecordingError

class DemonstrationTests(unittest.TestCase):
    def test_real_crash_restart_and_control_scenarios(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = run(Path(tmp) / 'run')
            self.assertTrue(all(evidence['checks'].values()))
            phases = [r['phase'] for r in evidence['crash_ledger_scan']['records']]
            self.assertNotIn('EXECUTION_SUCCESS', phases)
            self.assertIn('EXECUTION_STARTED', phases)

    def test_tampered_record_blocks_callback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'ledger.jsonl'
            writer = AppendOnlyLedgerWriter(str(path))
            gate = SovereignExecutionGate(writer, PostureArbitrationEngine())
            gate.execute_governed_action('first', ['GREEN_NOMINAL'], lambda: None)
            path.write_text(path.read_text().replace('GREEN_NOMINAL', 'BLACK_ABORT'))
            called = []
            with self.assertRaises(GovernanceDeniedError):
                gate.execute_governed_action('second', ['GREEN_NOMINAL'], lambda: called.append(True))
            self.assertEqual(called, [])

    def test_completion_error_is_not_a_general_persistent_freeze(self):
        # Document a material boundary of the current core, rather than hide it.
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            writer = AppendOnlyLedgerWriter(str(directory / 'ledger.jsonl'))
            gate = SovereignExecutionGate(writer, PostureArbitrationEngine())
            original = writer.write_entry
            def fail_success(record):
                return False if record['phase'] == 'EXECUTION_SUCCESS' else original(record)
            with patch.object(writer, 'write_entry', side_effect=fail_success):
                with self.assertRaises(CompletionRecordingError):
                    gate.execute_governed_action('first', ['GREEN_NOMINAL'], effect, directory)
            self.assertEqual(writer.scan_integrity()['unresolved_invocations'], [])
            gate.execute_governed_action('second', ['GREEN_NOMINAL'], lambda: None)

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileExistsError):
                run(Path(tmp))

if __name__ == '__main__':
    unittest.main()
