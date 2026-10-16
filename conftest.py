"""Prefer the src-layout package over the legacy root-level traceguard.py."""
from pathlib import Path
import sys

SRC = str(Path(__file__).resolve().parent / "src")
if SRC in sys.path:
    sys.path.remove(SRC)
sys.path.insert(0, SRC)
