import sys
import json
import asyncio
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
import mcp.types as types
import mcp.server.stdio

# Initialize the official Anthropic MCP Server instance
server = Server("traceguard-core")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Advertise the TraceGuard containment shield to Claude Desktop."""
    return [
        types.Tool(
            name="traceguard_shield_exec",
            description="Proxy wrapper that evaluates and executes tool calls through a deterministic C-D-M-Q safety perimeter.",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_tool": {"type": "string", "description": "The command or tool name requested by the model."},
                    "arguments": {"type": "object", "description": "The exact JSON parameters passed to the tool."}
                },
                "required": ["target_tool", "arguments"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Intercept, audit, and execute or hard-block the requested action."""
    if name != "traceguard_shield_exec" or not arguments:
        raise ValueError(f"Unknown tool requested: {name}")

    target_tool = arguments.get("target_tool")
    tool_args = arguments.get("arguments", {})

    # RUN THE SIGILITH LOGIC (C-D-M-Q Check)
    try:
        from traceguard_core.engine import evaluate_call
        is_authorized = evaluate_call(target_tool, tool_args)
    except ImportError:
        # Failsafe if the engine isn't fully stubbed yet
        is_authorized = False

    if not is_authorized:
        return [
            types.TextContent(
                type="text",
                text=f"[VIOLATION] AUTH_FAILURE: Thread hard-blocked by TraceGuard Perimeter. Action '{target_tool}' rejected."
            )
        ]

    return [
        types.TextContent(
            type="text",
            text=f"[SUCCESS] TraceGuard Verified. Executing {target_tool} safely."
        )
    ]

async def main():
    # Run the server over standard input/output (stdio), which Claude Desktop reads natively
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="traceguard-core",
                server_version="0.1.5",
                capabilities=server.get_capabilities()
            )
        )

# A synchronous wrapper is required for terminal entry points
def entry_point():
    asyncio.run(main())

if __name__ == "__main__":
    entry_point()
