import sys
import json
import difflib
import shutil
from pathlib import Path

def run_review(task_id: str):
    base_path = Path(f"staging/derekreviewqueue/{task_id}")
    if not base_path.exists():
        print(f"Task {task_id} not found in staging queue.")
        return

    # Load metadata
    metadata_path = base_path / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    print(f"\n=== SOVEREIGN REVIEW: {task_id} ===")
    print(f"Risk Level: {metadata.get('risk_level')}")
    print(f"Trigger Files: {', '.join(metadata.get('trigger_files', []))}")
    print(f"Rationale: {metadata.get('derek_decision', {}).get('message')}\n")

    snapshot_dir = base_path / "snapshot"
    proposed_dir = base_path / "proposed"

    # Diff each proposed file
    for proposed_file in proposed_dir.rglob("*"):
        if not proposed_file.is_file():
            continue

        rel_path = proposed_file.relative_to(proposed_dir)
        snapshot_file = snapshot_dir / rel_path

        print(f"--- DIFF: {rel_path} ---")

        if snapshot_file.exists():
            old_lines = snapshot_file.read_text(encoding="utf-8").splitlines(keepends=True)
            new_lines = proposed_file.read_text(encoding="utf-8").splitlines(keepends=True)

            diff = difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile=f"snapshot/{rel_path}",
                tofile=f"proposed/{rel_path}"
            )
            sys.stdout.writelines(diff)
        else:
            print(f"[NEW FILE]")
            print(proposed_file.read_text(encoding="utf-8"))

    # Sovereign override gate
    choice = input("\nApply these changes to live repo and append override to vault? [y/N]: ")

    if choice.lower() == 'y':
        # Apply proposed changes to live repo
        for proposed_file in proposed_dir.rglob("*"):
            if proposed_file.is_file():
                rel_path = proposed_file.relative_to(proposed_dir)
                live_path = Path(rel_path)
                live_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(proposed_file, live_path)

        # Append EXECUTION_APPROVED to ledger
        ledger_entry = {
            "event": "EXECUTION_APPROVED",
            "task_id": task_id,
            "metadata": metadata
        }

        ledger_path = Path("traceguard_async_ledger.jsonl")
        existing = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
        ledger_path.write_text(existing + json.dumps(ledger_entry) + "\n", encoding="utf-8")

        # Remove staging task
        shutil.rmtree(base_path)

        print("Override approved. Changes applied and anchored to vault.")
    else:
        print("Override denied. Task remains in staging.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m three_lineage.reviewtask <task_id>")
    else:
        run_review(sys.argv[1])
