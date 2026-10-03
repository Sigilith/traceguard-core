# TraceGuard — inspect the failure boundary

**The action happened. The receipt didn't. What happens next?**

[Run The Missing Receipt demonstration](examples/missing_receipt/README.md): a worker writes a local delivery, dies before recording completion, and a fresh process attempts execution. Compare the effect against the ledger and inspect the restart decision.

```sh
python3 examples/missing_receipt/demo.py run --output ./missing-receipt-run
python3 -m unittest discover -s examples/missing_receipt/tests -v
```

Python 3.10+ on Linux/Termux; no dependencies, credentials or network calls. Use a new output directory each run.

This is an isolated demonstration of the supplied ThreeLineage-Core execution-gate snapshot, **not an integration into the current MCP gateway or a guarantee about every runtime in this repository**. See its [claim and limitations](examples/missing_receipt/README.md), [integration guide](examples/missing_receipt/INTEGRATION.md) and [implementation service scope](examples/missing_receipt/COMMERCIAL.md).

---

## 🛡️ Secure Claude Desktop with TraceGuard

TraceGuard can be deployed immediately as a Model Context Protocol (MCP) gateway to intercept, audit, and validate commands before Claude Desktop can execute them on your local system.

### One-Click Configuration

Add the following configuration to your Claude Desktop config file to automatically run TraceGuard as your secure perimeter.

**Config Locations:**
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "traceguard-perimeter": {
      "command": "uvx",
      "args": ["traceguard-core"]
    }
  }
}
```

# TraceGuard

TraceGuard is a zero-trust governance and audit framework providing:
- Action verification
- Ledger integrity
- AXIOMOS risk scoring
- Compliance reporting
- CLI demo

## Installation
    pip install traceguard

## Examples
See the `examples/` directory.

## Documentation
See the `docs/` directory.

## CLI
    traceguard demo


