import pytest
import asyncio
from traceguard.middleware import TraceGuardMiddleware

@pytest.mark.asyncio
async def test_middleware_allowed_action():
    middleware = TraceGuardMiddleware(allowed_actions=["safe_query"])
    def mock_tool():
        return "success_data"
    
    res = await middleware.execute_protected_action("agent_1", "safe_query", mock_tool)
    assert res["status"] == "EXECUTED"
    assert res["result"] == "success_data"
    assert "provenance_hash" in res

@pytest.mark.asyncio
async def test_middleware_blocked_action():
    middleware = TraceGuardMiddleware(allowed_actions=["safe_query"])
    def mock_tool():
        return "should_not_run"
    
    res = await middleware.execute_protected_action("agent_1", "unauthorized_drop", mock_tool)
    assert res["status"] == "CONTAINED"
    assert res["risk_tier"] is not None
    assert "provenance_hash" in res
