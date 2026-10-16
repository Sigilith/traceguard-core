# TraceGuard Core

TraceGuard Core includes a Python governance/evidence library and an optional MCP action-name gate.

## MCP gate scope

        "TRACEGUARD_ALLOWED_ACTIONS": "[\"read_logs\"]"

Example configuration:

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

## Install

After the 0.1.7 release is published:

```sh
python -m pip install traceguard-core==0.1.7
```

The distribution name is `traceguard-core`; the core Python package is `traceguard` and the MCP adapter is `traceguard_core`.

## Development tests

Pytest is configured to put `src/` first on the import path, preventing the legacy root-level `traceguard.py` script from shadowing the `traceguard` package during collection. The release checks run the package contract tests directly; unrelated legacy integration tests are not part of this package test command.

```sh
python -m pip install -e '.[test]'
python -m pytest -q tests/test_engine_extra.py tests/test_mcp_gate.py
```
