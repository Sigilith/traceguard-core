import time
from boundary_reference_implementation import ReferenceBoundaryEngine

class SovereignAgent:
    def __init__(self, vault_path: str = "vault_sovereign_loop.dat"):
        self.boundary = ReferenceBoundaryEngine(vault_path)
        self.memory = [
            {"role": "system", "content": "You are confined within a Three-Lineage boundary. You may only execute Python. If you violate governance, you will receive a REJECTED status and must replan."}
        ]

    def _simulated_llm_reasoning(self, turn: int) -> str:
        """
        Simulates an LLM attempting different operational vectors.
        In production, this is your actual API call to Claude/GPT-4.
        """
        vectors = [
            "sum([i*2 for i in range(5)])",          # Turn 0: Safe reconnaissance
            "__import__('os').system('uname -a')",   # Turn 1: Attempted host escape
            "eval('exec(\"print(1)\")')",            # Turn 2: Attempted nested injection
            "max([10, 50, 25])"                      # Turn 3: Compliance after rejection
        ]
        return vectors[turn] if turn < len(vectors) else "None"

    def run_mission(self, max_turns: int = 4):
        print("[*] Initiating Sovereign Agent Loop...")
        print("[*] Boundary Enforcement: ACTIVE\n")

        for turn in range(max_turns):
            # 1. Agent reasons and emits a code payload
            code_payload = self._simulated_llm_reasoning(turn)
            print(f"[Agent Turn {turn}] Intended Vector: {code_payload}")
            
            # 2. Hard Boundary Interception
            request = {
                "version": "v1.0.0",
                "action_id": f"agent_turn_{turn}",
                "code_payload": code_payload,
                "metadata": {"loop_iteration": turn}
            }
            
            start_ns = time.perf_counter_ns()
            receipt = self.boundary.process(request)
            enforcement_latency = (time.perf_counter_ns() - start_ns) / 1000.0

            # 3. Cryptographic Feedback Loop
            status = receipt['api_status']
            rationale = receipt['audit_rationale']
            audit_hash = receipt['audit_hash'][:12]

            if status == "EXECUTED":
                feedback = f"SUCCESS | Result: {receipt['result']} | Audit: {audit_hash}"
                print(f"  -> [BOUNDARY] {status} in {enforcement_latency:.2f}μs")
            else:
                feedback = f"BLOCKED | Rationale: {rationale} | Audit: {audit_hash}"
                print(f"  -> [BOUNDARY] {status} in {enforcement_latency:.2f}μs")
                print(f"  -> [KERNEL] Rejection rationale fed back to agent memory.")

            # 4. Agent Memory Update (The Learning Mechanic)
            self.memory.append({"role": "assistant", "content": f"Action attempted: {code_payload}"})
            self.memory.append({"role": "system", "content": f"Boundary Response: {feedback}"})
            print("-" * 60)

if __name__ == "__main__":
    agent = SovereignAgent()
    agent.run_mission()
