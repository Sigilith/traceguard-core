# THREE-LINEAGE OPERATIONAL PROCEDURES
**Architecture State:** LOCKED (OS-Level Immutability via chmod 444)
**Core Invariant:** STRICT DENY / FAIL-CLOSED

Due to the physical lockdown of the Three-Lineage governance boundary, standard git pushes or agent-led edits to core enforcement files are fundamentally blocked. All modifications must follow this strict three-phase operational procedure.

## Phase 1: Proposal & Simulation (Staging)
1. **Agent Isolation:** Derek and all subordinate agents are strictly prohibited from writing to `three_lineage/core/` or `three_lineage/aximos/`.
2. **Offline Drafting:** Proposed governance patches must be staged in a physically separate sandbox (`staging/drafts/`).
3. **Fuzz Verification:** Before a patch can be submitted for physical integration, it must pass the continuous boundary fuzzer to prove that malformed contexts do not trigger a `fail_open` bypass.

## Phase 2: Auditing & Cryptographic Verification
1. **Hash Ledger Verification:** Run `sha256sum` against the current locked files to establish the pre-patch baseline.
2. **Invariant Proofing:** Ensure the patch maintains the `fail_closed=True` state in `governance.py`.
3. **Gate Review:** Ensure the time-bound cryptographic nonce logic in `derek_gate.py` (5-second expiration) is not widened or bypassed.

## Phase 3: Application & Re-locking
Modifications require manual OS-level intervention by a superuser.
1. **Unlock:** `chmod 644 three_lineage/aximos/*.py three_lineage/core/*.py staging/derekreviewqueue/immune_intercept/*.json`
2. **Patch & Test:** Apply the patch, execute the test suite to ensure the sliding window and gate validations pass.
3. **Re-Lock:** `chmod 444 three_lineage/aximos/*.py three_lineage/core/*.py staging/derekreviewqueue/immune_intercept/*.json`
4. **Reseal Ledger:** Commit the new SHA256 hashes to the append-only genesis ledger.
