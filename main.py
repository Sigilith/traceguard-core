from src.traceguard import TraceGuard
from src.aximos import AXIOMOSEvaluator
from src.matrix import AssuranceMatrix

def main():
    print("Initializing TraceGuard Engine...")
    tg = TraceGuard(allowed_actions=["read_logs", "safe_query"])
    
    print("Evaluating actions...")
    print(f"Action 'safe_query': {tg.evaluate_action('safe_query')}")
    print(f"Action 'unauthorized_shell_exec': {tg.evaluate_action('unauthorized_shell_exec')}")
    print(f"Action 'delete_system_root': {tg.evaluate_action('delete_system_root')}")
    
    ax = AXIOMOSEvaluator(block_threshold=2)
    risk = ax.evaluate_logs(tg.get_logs())
    print(f"AXIOMOS Risk Classification: {risk}")
    
    matrix = AssuranceMatrix()
    tier_info = matrix.calculate_tier(consequence=3, autonomy=2, oversight=False)
    print(f"Assurance Matrix Result: {tier_info}")

if __name__ == "__main__":
    main()
