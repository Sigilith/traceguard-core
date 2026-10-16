"""MCP adapter that returns allow/block decisions and never executes tools."""
import asyncio

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions

from traceguard_core import __version__
from traceguard_core.engine import evaluate_call, parse_allowed_actions

server = Server("traceguard-core")

try:
    _ALLOWED_ACTIONS = parse_allowed_actions()
except ValueError:
    # Invalid policy configuration is treated as an empty allowlist.
    _ALLOWED_ACTIONS = frozenset()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Expose an explicit decision-only tool; execution remains with the caller."""
    return [
        types.Tool(
            name="traceguard_check_action",
            description=(
                "Return ALLOW or BLOCK for an exact action name using the configured "
                "TRACEGUARD_ALLOWED_ACTIONS allowlist. This tool does not execute the action. "
                "Arguments are not checked against per-tool schemas."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target_tool": {"type": "string"},
                    "arguments": {"type": "object"},
                },
                "required": ["target_tool", "arguments"],
                "additionalProperties": False,
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name != "traceguard_check_action" or not isinstance(arguments, dict):
        raise ValueError(f"Unknown tool or malformed request: {name}")

    target_tool = arguments.get("target_tool")
    tool_args = arguments.get("arguments")
    allowed = evaluate_call(target_tool, tool_args, _ALLOWED_ACTIONS)
    decision = "ALLOW" if allowed else "BLOCK"
    detail = "action name is allow-listed" if allowed else "action is not allow-listed or request is malformed"
    return [
        types.TextContent(
            type="text",
            text=f"{decision}: {detail}. Decision only; no tool was executed.",
        )
    ]


async def main() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="traceguard-core",
                server_version=__version__,
                capabilities=server.get_capabilities(),
            ),
        )


def entry_point() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    entry_point()
