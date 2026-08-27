#!/bin/bash

# Create directories
mkdir -p src
mkdir -p tests

# Create cli.py
cat << 'EOF2' > cli.py
# CLI ENTRYPOINT
# (Minimal placeholder so packaging works)
def main():
    print("TraceGuard CLI is installed and working.")
EOF2

# Create pyproject.toml
cat << 'EOF3' > pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "traceguard"
version = "1.0.0"
description = "Deterministic containment, behavioral drift evaluation, and tamper-evident compliance for autonomous agents."
readme = "README.md"
requires-python = ">=3.8"
dependencies = ["fpdf2>=2.7.0", "pytest>=7.0.0"]

[project.scripts]
traceguard = "cli:main"

[tool.setuptools]
packages = ["src"]
py-modules = ["cli"]
EOF3

# Create README.md
cat << 'EOF4' > README.md
# TraceGuard Core

Deterministic containment, behavioral drift evaluation, and tamper-evident compliance for autonomous agent systems.

## Installation

```bash
git clone https://github.com/Sigilith/traceguard-core.git
cd traceguard-core
pip install .
