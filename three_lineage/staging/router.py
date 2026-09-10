import os
import json
import shutil
import uuid
from pathlib import Path

class StagingRouter:
    """
    Sovereign staging router for ThreeLineage.
    Creates isolated review tasks when Derek halts execution.
    """

    def __init__(self, base_dir: str = "staging/derekreviewqueue"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_task(self, metadata: dict, proposed_files: dict):
        """
        Create a sovereign staging task.
        metadata: dict containing risk_level, trigger_files, derek_decision, etc.
        proposed_files: { "relative/path.py": "new file contents" }
        """

        # Generate unique task ID
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        task_path = self.base_dir / task_id
        snapshot_path = task_path / "snapshot"
        proposed_path = task_path / "proposed"

        # Create directories
        snapshot_path.mkdir(parents=True, exist_ok=True)
        proposed_path.mkdir(parents=True, exist_ok=True)

        # Write metadata.json
        (task_path / "metadata.json").write_text(
            json.dumps(metadata, indent=4),
            encoding="utf-8"
        )

        # Write proposed files + snapshot originals
        for rel_path, new_content in proposed_files.items():
            rel = Path(rel_path)

            # Proposed file
            proposed_file = proposed_path / rel
            proposed_file.parent.mkdir(parents=True, exist_ok=True)
            proposed_file.write_text(new_content, encoding="utf-8")

            # Snapshot file (copy from live repo if exists)
            live_file = Path(rel)
            snapshot_file = snapshot_path / rel
            snapshot_file.parent.mkdir(parents=True, exist_ok=True)

            if live_file.exists():
                shutil.copy2(live_file, snapshot_file)
            else:
                snapshot_file.write_text("", encoding="utf-8")

        return {
            "task_id": task_id,
            "task_path": str(task_path)
        }
