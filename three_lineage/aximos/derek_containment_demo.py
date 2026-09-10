#!/usr/bin/env python3

"""
DEREK / Three-Lineage Containment Demonstration v1

Sigilith   -> structural observation
TraceGuard -> execution boundary + evidence
AXIOMOS    -> policy / authority decision
Derek      -> reproducible containment receipt

This runner does NOT invent PASS/FAIL values.
It records what the underlying Three-Lineage test actually reports.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINEAGE = ROOT / ".lineage"
LEDGER = LINEAGE / "collisions.jsonl"
RECEIPTS = LINEAGE / "derek_receipts"
RECEIPTS.mkdir(parents=True, exist_ok=True)

RUN_ID = str(uuid.uuid4())
START = datetime.now(timezone.utc).isoformat()


def sha256_file(path):
    if not path.exists():
        return None

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_campaign():
    p = ROOT / "test_compound_campaign.sh"
    return p if p.exists() else None


def verifier():
    binary = ROOT / "lineage_check" / "target" / "release" / "lineage_check"

    if not binary.exists():
        print("[CRITICAL] Rust verifier binary not found.")
        return 1, ""

    if not LEDGER.exists():
        print("[CRITICAL] TraceGuard ledger missing.")
        return 1, ""

    command = [str(binary), str(LEDGER)]

    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    output = result.stdout + result.stderr
    print(output, end="")

    return result.returncode, output


def extract(pattern, text, default="UNKNOWN"):
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else default


def run_campaign(path):
    print()
    print("[*] DEREK CONTAINMENT DEMONSTRATION")
    print(f"[*] Campaign: {path.relative_to(ROOT)}")
    print(f"[*] Run ID:   {RUN_ID}")
    print()

    # Run the shell campaign with bash, not python
    result = subprocess.run(
        ["bash", str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    output = result.stdout + result.stderr
    print(output)

    return result.returncode, output


def build_receipt(
    campaign,
    campaign_output,
    campaign_exit,
    initial_verifier_exit,
    final_verifier_exit,
    initial_ledger_hash,
    final_ledger_hash,
):
    tests = {
        "unknown_contract": extract(
            r"Unknown Contract ID.*?\n.*?Status:\s*([A-Z0-9_ -]+)",
            campaign_output,
        ),
        "replay": extract(
            r"Replay Status:\s*([A-Z0-9_ -]+)",
            campaign_output,
        ),
        "intent_drift": extract(
            r"Lane Escalation Status:\s*([A-Z0-9_ -]+)",
            campaign_output,
        ),
        "forbidden_domain": extract(
            r"Forbidden Domain Status:\s*([A-Z0-9_ -]+)",
            campaign_output,
        ),
        "expired_contract": extract(
            r"Expired Contract Status:\s*([A-Z0-9_ -]+)",
            campaign_output,
        ),
        "concurrent_execution": extract(
            r"Concurrent Race Results:\s*(.*)",
            campaign_output,
        ),
        "post_restart_replay": extract(
            r"Post-Restart Replay Status:\s*([A-Z0-9_ -]+)",
            campaign_output,
        ),
    }

    tamper_detected = (
        "Hash chain fracture" in campaign_output
        or "Verifier Exit Code: 1" in campaign_output
        or "CRITICAL" in campaign_output
    )

    receipt = {
        "receipt_type": "DEREK_CONTAINMENT_RECEIPT",
        "version": "1.0",
        "run_id": RUN_ID,
        "timestamp_utc": START,

        "system": {
            "name": "Three-Lineage",
            "agent": "Derek",
        },

        "pipeline": {
            "structural_layer": "Sigilith",
            "evidence_layer": "TraceGuard",
            "decision_layer": "AXIOMOS",
        },

        "campaign": {
            "script": str(campaign.relative_to(ROOT)),
            "exit_code": campaign_exit,
        },

        "tests": tests,

        "traceguard": {
            "ledger": str(LEDGER.relative_to(ROOT)),
            "initial_ledger_sha256": initial_ledger_hash,
            "final_ledger_sha256": final_ledger_hash,
        },

        "verifier": {
            "initial_exit_code": initial_verifier_exit,
            "final_exit_code": final_verifier_exit,
            "tamper_detected": tamper_detected,
        },

        "result": {
            "execution_escape_claimed": False,
            "containment_verified": final_verifier_exit == 1,
            "cryptographic_integrity_claimed": initial_verifier_exit == 0,
        },
    }

    out_path = RECEIPTS / f"{RUN_ID}.json"
    with out_path.open("w") as f:
        json.dump(receipt, f, indent=4)

    print()
    print(f"[+] Receipt SHA-256: {sha256_file(out_path)}")
    print(f"[+] Receipt written: {out_path}")

    return out_path


def main():
    campaign = find_campaign()
    if not campaign:
        print("[CRITICAL] No campaign script found.")
        sys.exit(1)

    print("============================================================")
    print("       DEREK / CONTAINMENT DEMONSTRATION v1")
    print("============================================================")
    print(f"Run ID: {RUN_ID}")
    print()
    print(f"[+] Located campaign: {campaign.name}")
    print()

    print("[*] PRE-BOOT TRACEGUARD VERIFICATION")
    initial_verifier_exit, initial_output = verifier()
    initial_ledger_hash = sha256_file(LEDGER)

    if initial_verifier_exit != 0:
        print("[CRITICAL] PRE-BOOT INTEGRITY GATE FAILED.")
        print("[CRITICAL] Derek will NOT claim a clean demonstration.")
        sys.exit(1)

    campaign_exit, campaign_output = run_campaign(campaign)

    print()
    print("[*] POST-RUN TRACEGUARD VERIFICATION")
    final_verifier_exit, final_output = verifier()
    final_ledger_hash = sha256_file(LEDGER)

    build_receipt(
        campaign,
        campaign_output,
        campaign_exit,
        initial_verifier_exit,
        final_verifier_exit,
        initial_ledger_hash,
        final_ledger_hash,
    )


if __name__ == "__main__":
    main()
