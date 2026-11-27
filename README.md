# TraceGuard Core

**Action governance, evidence handling and an optional MCP policy gate.**

TraceGuard Core is a Python project from Sigilith. It contains a governance/evidence library and an MCP adapter that makes an allow/block decision for an exact action name.

The MCP adapter is deliberately decision-only: it does **not** execute the requested action. The calling application remains responsible for execution and for enforcing the decision.

## What is included

- **Python library** — governance and evidence components exposed through the `traceguard` package.
- **MCP adapter** — the `traceguard_core` server exposes `traceguard_check_action`.
- **Explicit allowlist** — action names are checked against `TRACEGUARD_ALLOWED_ACTIONS`.
- **Fail-closed configuration** — a missing or invalid allowlist does not grant permission.
- **Tests** — focused package and MCP-gate regression tests.

## MCP policy gate

The adapter returns a decision for an exact action name. It does not execute tools, inspect arguments against each target tool's schema, or provide an operating-system sandbox.

Example MCP client configuration:

```json
{
  "mcpServers": {
    "traceguard-core": {
      "command": "uvx",
      "args": ["traceguard-core"],
      "env": {
        "TRACEGUARD_ALLOWED_ACTIONS": "[\"read_logs\"]"
      }
    }
  }
}
```

Only the action names explicitly listed in `TRACEGUARD_ALLOWED_ACTIONS` are eligible for an ALLOW decision. Start with the smallest required allowlist. Treat the returned decision as one control in a wider execution design, not as a substitute for enforcement at the actual execution boundary.

## Development setup

Use a supported Python version (3.10 or later).

```sh
git clone https://github.com/Sigilith/traceguard-core.git
cd traceguard-core
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[test]'
python -m pytest -q tests/test_engine_extra.py tests/test_mcp_gate.py
```

The test configuration places `src/` first on the import path so the package tests do not accidentally import the legacy root-level `traceguard.py` script.

## Package names

| Purpose | Name |
| --- | --- |
| Python distribution | `traceguard-core` |
| Governance/evidence package | `traceguard` |
| MCP adapter package | `traceguard_core` |
| MCP executable | `traceguard-core` |

Check the [PyPI project page](https://pypi.org/project/traceguard-core/) for the currently published distribution. Do not assume that the version on the development branch is already published.

## Security and assurance boundaries

- The MCP adapter makes an action-name decision; it does not execute or contain the target action.
- The adapter does not validate arguments against the target tool's schema.
- A caller that ignores or bypasses the decision is outside the adapter's enforcement.
- This repository is not a security certification, compliance attestation, or guarantee that a deployment is secure.
- Deployment guarantees depend on the surrounding application, operating system, storage, key management and execution architecture.

See [SECURITY.md](SECURITY.md) for vulnerability reporting guidance. Please use synthetic data in demonstrations and tests; never commit credentials, private keys, customer data or production secrets.

## Contributing

Focused fixes and reproducible tests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Project

Maintained by [Sigilith](https://github.com/Sigilith). The wider ThreeLineage architecture and its other components are developed separately; this repository does not publish the complete integrated runtime.
