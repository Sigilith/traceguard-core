
from pathlib import Path
import ast

class SigilithObserverAgent:
    """
    Structural observation arm of ThreeLineage.
    Produces syntactic + structural telemetry for TraceGuard.
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def observe_codebase(self):
        observations = []
        for py_file in self.repo_path.rglob("*.py"):
            # Skip virtual environments and git internals
            if "venv" in py_file.parts or ".git" in py_file.parts:
                continue

            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
                observations.append({
                    "file": str(py_file.relative_to(self.repo_path)),
                    "classes": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                    "functions": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
                })
            except Exception as e:
                observations.append({
                    "file": str(py_file),
                    "error": str(e)
                })

        return {
            "source": str(self.repo_path),
            "telemetry": observations
        }
