# ThreeLineage: The Missing Receipt

**The action happened. The receipt didn't. What happens next?**

A runnable incident demonstration of a separately supplied ThreeLineage-Core snapshot. A worker writes a delivery, dies before recording completion, and a fresh process attempts execution. This example is isolated from this repository's current MCP gateway and runtime.

## Inspect the evidence

Read the captured [incident timeline](sample-run/timeline.txt), [machine-readable checks](sample-run/evidence.json), and [crash ledger](sample-run/crash/ledger.jsonl). Then reproduce the behavior yourself.

| Scenario | Observable result |
|---|---|
| Normal execution | One delivery and a completion record |
| BLACK_ABORT veto | No delivery |
| Reservation fsync failure | No delivery; ledger bytes may already exist |
| Worker dies after delivery | One delivery; unresolved EXECUTION_STARTED |
| Fresh process attempts execution | Denied; delivery count stays at one |
| Deliberately naive retry | Two deliveries |

## Reproduce it

Python 3.10+ on Linux or Termux. Standard library only; no credentials, dependencies or network calls. Use a filesystem with working locks and fsync. From the repository root:

```sh
cd examples/missing_receipt
python3 demo.py run --output ./my-first-run
python3 -m unittest discover -s tests -v
cat my-first-run/timeline.txt
```

Use a new output directory each run; existing directories are rejected to preserve evidence. Inspect its `evidence.json`, `crash/ledger.jsonl` and `crash/deliveries.txt`. The included sample is a captured run, not a substitute for rerunning locally.

## The precise claim

An unresolved `EXECUTION_STARTED` prevents subsequent reservations through `SovereignExecutionGate` using the same intact ledger. In the demonstrated crash window, restart does not automatically repeat the side effect.

This is a tested behavior, not a formal proof, an exactly-once guarantee, or a claim of market uniqueness.

## Challenge the claim

Try to produce a second callback execution through this gate while the same intact ledger still contains an unresolved `EXECUTION_STARTED`. Report the source revision, Python and OS versions, reproduction steps, ledger and observed side effect. Use synthetic local data only.

Calling the callback directly, replacing the ledger, or choosing another ledger changes an explicit assumption. Other failure modes are still useful findings; identify which assumption they change. A passing suite does not prove that no counterexample exists.

## Assumptions and limitations

- Relevant work must use this gate and the same ledger. It does not contain arbitrary code or prevent direct callback invocation.
- The callback flushes its local effect with fsync before `os._exit(77)`. This tests abrupt process death, not power failure or every storage implementation.
- An external side effect and its ledger receipt are not atomically committed. Reconciliation remains necessary; the demo leaves the crashed invocation unresolved.
- The ledger is hash-linked, not independently authenticated. An actor able to rewrite and rehash the entire file can change history. No external anchor or TraceGuard daemon is included.
- `EXECUTION_FAILED_AFTER_START` and `COMPLETION_RECORDING_FAILED` are terminal states in this snapshot. If successfully recorded, later reservations can proceed. A dedicated test exposes this limitation.
- A reservation persistence failure can leave bytes behind. It is not evidence of rollback or permission to retry blindly.
- An unresolved intent blocks all reservations on that ledger, imposing an availability cost. Recovery and isolation need system-specific design.
- The unsafe comparison deliberately retries a non-idempotent operation; it is not a competitor benchmark.

## Integrate and evaluate

See the [integration guide](INTEGRATION.md), [source provenance](PROVENANCE.json), and separate [paid implementation scope](COMMERCIAL.md). The core files are copied unchanged from an owner-supplied snapshot. The hosting repository base commit is recorded separately; it is not the core snapshot's source commit. No production deployment is claimed.

## Attribution and licensing

ThreeLineage framework attribution: Ky Nash / ThreeLineage, as supplied by the project owner. Demonstration, tests and documentation assembled with AI assistance. Exact core hashes are recorded in provenance.

The hosting repository declares MIT in package metadata, but its LICENSE currently contains only an MIT heading. This example does not amend that file or settle the separately supplied snapshot's licensing. Confirm complete terms and preserve upstream notices before downstream redistribution. No endorsement by Google, AISI or another organisation is claimed.
