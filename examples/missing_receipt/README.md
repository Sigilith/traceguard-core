# ThreeLineage: The Missing Receipt

**The action happened. The receipt didn't. What happens next?**

A small executable incident demonstration of a separately supplied ThreeLineage-Core snapshot. It is isolated from this repository's current MCP gateway and runtime. Watch a worker durably append a delivery, terminate before recording completion, and restart. Inspect whether a second delivery is allowed.

## Run in under a minute

Python 3.10+ on Linux or Termux. Standard library only; no API keys, accounts, payment services or network calls. Run in a local directory with working file locking and fsync.

```sh
python3 demo.py run --output ./my-first-run
python3 -m unittest discover -s tests -v
cat my-first-run/timeline.txt
```

Choose a new output directory each time. Existing directories are rejected to preserve evidence. `sample-run/` contains a captured run, not a substitute for rerunning locally.

## What to inspect

| Scenario | Expected observable result |
|---|---|
| Normal execution | One delivery and a completion record |
| BLACK_ABORT vote | No delivery |
| Reservation fsync failure | No delivery, although ledger bytes may already exist |
| Worker exits after delivery | One delivery; unresolved EXECUTION_STARTED |
| Fresh process attempts execution | Denied; delivery count remains one |
| Deliberately naive retry | Two deliveries |

Open `evidence.json` for acceptance checks, errors, runtime, core hashes and the crash ledger scan. Open `crash/ledger.jsonl` and `crash/deliveries.txt` to compare the record of intent against the actual local effect. The harness checks outcomes; it does not merely print a scripted success story.

## Precise claim

In this supplied core snapshot, an unresolved `EXECUTION_STARTED` record prevents subsequent execution reservations through `SovereignExecutionGate` using the same ledger. In the demonstrated crash window, restarting does not automatically repeat the side effect.

This is a reproducible test of one behavior, not a formal proof or an exactly-once execution guarantee.

## Assumptions and limits

- All relevant work must use this gate and the same intact ledger. Direct callback invocation, another ledger, or an actor rewriting the ledger bypasses this boundary.
- The callback's local effect is flushed with fsync before abrupt process exit using `os._exit(77)`. This tests process death, not a power failure or every filesystem/storage implementation.
- The gate cannot atomically commit an arbitrary external effect and its ledger receipt. Reconciliation remains necessary. This demo deliberately leaves the crashed invocation unresolved.
- This ledger is hash-linked, not independently authenticated. A writer controlling the whole file can rewrite and rehash history. This package includes no external trust anchor or TraceGuard service.
- `EXECUTION_FAILED_AFTER_START` and `COMPLETION_RECORDING_FAILED` are terminal states in this core. If such a record is successfully written, later reservations can proceed. One test preserves this limitation visibly.
- A reservation persistence failure can leave bytes in a file; it must not be interpreted as a clean rollback or permission to retry blindly.
- The unresolved intent blocks all reservations on that ledger, with an availability cost. Production designs need a defined recovery process and suitable isolation.
- The unsafe comparison is deliberately naive automatic retry. It is not a comparison against a named competitor or evidence of market uniqueness.

## Why this demonstration is useful

An integrator gets an observable business failure: a delivery happened but the normal completion receipt is absent. They can inspect both artifacts, reproduce the crash and evaluate the restart decision. The project makes a narrow promise and exposes the point where human or system-specific reconciliation is still required.

See `INTEGRATION.md`, `COMMERCIAL.md` and `PROVENANCE.json`. The core files are copied unchanged from the ThreeLineage snapshot available in this conversation. The hosting repository base commit is recorded separately in provenance; it is not the source commit of these core files. No production deployment is claimed.

## Attribution and licensing

ThreeLineage framework attribution: Ky Nash / ThreeLineage, as supplied by the project owner. The demonstration, tests and documentation were assembled with AI assistance. Core file hashes identify the exact reviewed snapshot.

The hosting repository declares MIT in its package metadata, but its current LICENSE contains only the heading “MIT License”. This example does not amend that file or settle the separate core snapshot's licensing. Confirm complete licence terms and preserve upstream notices before downstream redistribution. Do not imply Google, AISI or another organisation endorses this work.
