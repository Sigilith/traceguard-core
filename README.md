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

