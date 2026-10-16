from traceguard_core.mcp_server import _build_initialization_options


def test_startup_initialization_options_include_registered_tool_capability():
    options = _build_initialization_options()

    assert options.server_name == "traceguard-core"
    assert options.server_version
    assert options.capabilities.tools is not None
