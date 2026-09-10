import asyncio
from inspect_ai.solver import TaskState
from arena_solver import threelineage_governance_solver

async def run_test():
    print("[+] Initializing ThreeLineage ControlArena Solver Test...")
    solver_fn = threelineage_governance_solver()
    
    # Mock a basic TaskState to simulate an agent environment tick
    state = TaskState(
        sample_id=1,
        epoch=0,
        input="Test safety prompt",
        messages=[],
        model="mock",
        output=None,
        completed=False
    )
    
    # Execute the solver step
    result_state = await solver_fn(state, None)
    print(f"    State Completed: {result_state.completed}")
    print(f"    Completion Output: {result_state.output.completion}")
    print("[+] ControlArena Solver Bridge Verified.")

asyncio.run(run_test())
