# Integration boundary

The public API exercised here is:

```python
from core.ledger_writer import AppendOnlyLedgerWriter
from core.arbitration_engine import SovereignExecutionGate, PostureArbitrationEngine

writer = AppendOnlyLedgerWriter('/absolute/private/state/ledger.jsonl')
gate = SovereignExecutionGate(writer, PostureArbitrationEngine())
result = gate.execute_governed_action(
    'your-operation', ['GREEN_NOMINAL'], your_callback
)
```

Supply votes from your actual policy authority. Hardcoding GREEN_NOMINAL in a real application provides no useful policy decision. This example demonstrates the call boundary only.

1. Identify the exact side effect and give it a stable business operation identifier in your application. The core creates a fresh invocation UUID for each attempt; it does not provide business-level deduplication.
2. Keep the ledger private, persistent and shared by the workers intended to share this gate. Confirm filesystem locks and fsync behavior in your deployment.
3. Route every relevant side effect through the gate. Keep model-generated instructions separate from the authority deciding votes and from connector credentials.
4. Handle `GovernanceDeniedError` and `CompletionRecordingError` without automatic retries of potentially completed actions. A GovernanceDeniedError can also wrap an error after the callback starts; it does not always mean no effect occurred.
5. If an invocation is unresolved, preserve evidence and inspect the downstream system using its operation identifier. Decide whether the effect happened, did not happen, or remains unknown. The local demonstration cannot settle this for email, billing, deployments or APIs.
6. Design and test an explicit authorised reconciliation operation before deployment. Do not delete the ledger, fabricate a success receipt or silently discard an unresolved intent to restore availability.

Run the included tests first, then adapt crash injection to your own connector in a sandbox. Add provider-specific idempotency, downstream receipt verification and recovery rules where available. This package intentionally does not connect to payments or messaging accounts.

## Source map

- `core/`: unchanged supplied implementation.
- `demo.py`: process supervisor, crash injection, local effect and evidence capture.
- `tests/test_demo.py`: restart, integrity, failure semantics and evidence preservation tests.
- `sample-run/`: actual captured local run.

The demo worker uses os._exit so Python exception handling cannot write a terminal record. The supervisor starts a separate Python process for the restart attempt. Storage failure is injected at os.fsync; it is not a physical disk fault.
