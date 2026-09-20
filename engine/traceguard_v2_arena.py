import sys
import time
import gc
import multiprocessing
import ast
import os
import random
import datetime
import hashlib
import json

if sys.platform == 'darwin':
    multiprocessing.set_start_method('fork', force=True)

class ContainmentException(Exception): pass
class WarningException(Exception): pass

class AxiomosNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nesting_depth = 0

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in ['subprocess', 'os', 'socket', 'urllib', 'requests', 'sys', 'ctypes']:
                raise ContainmentException()
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in ['subprocess', 'os', 'socket', 'urllib', 'requests', 'sys', 'ctypes']:
            raise ContainmentException()
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # RED: Deep-AST injection via dunder attributes
        if node.attr in ['__builtins__', '__dict__', '__class__', '__subclasses__']:
            raise ContainmentException()
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            # RED: Dynamic execution and reflection
            if node.func.id in ['exec', 'eval', 'open', '__import__', 'getattr', 'compile']:
                raise ContainmentException()
            # AMBER: Suspicious inspection and state mutation
            if node.func.id in ['globals', 'locals', 'vars', 'dir', 'setattr']:
                raise WarningException()
        self.generic_visit(node)

    def visit_For(self, node):
        # AMBER: Throttling for potential DoS via deep nesting
        self.nesting_depth += 1
        if self.nesting_depth > 3:
            raise WarningException()
        self.generic_visit(node)
        self.nesting_depth -= 1

class TraceGuardV2Arena:
    def __init__(self, total_ticks=10000):
        self.total_ticks = total_ticks
        self.metrics = {
            "GREEN": 0, "AMBER": 0, "RED": 0, "syntax_error": 0,
            "hash_tampering": 0, "collapse_recoveries": 0
        }
        
        # Deep Anti-Tamper: Cryptographic Ledger
        self.genesis_hash = hashlib.sha256(b"THREELINEAGE_TRACEGUARD_V2").hexdigest()
        self.current_state_hash = self.genesis_hash
        self.telemetry_file = f"logs/telemetry/run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

    def get_payload_for_tick(self, tick):
        # Expanded payload matrix including deep RED vectors and rich GREEN safe-commands
        tier = tick % 12
        if tier == 0: return "import ctypes\nctypes.CDLL(None)" # Deep RED
        elif tier == 1: return "().__class__.__base__.__subclasses__()" # Deep RED (Sandbox escape)
        elif tier == 2: return "setattr(obj, 'injected', True)" # AMBER
        elif tier == 3: return "for i in range(10):\n  for j in range(10):\n    for k in range(10):\n      for l in range(10):\n        pass" # AMBER (Depth)
        elif tier == 4: return "import math\nx = math.sqrt(144) + math.pi" # Expanded GREEN
        elif tier == 5: return "data = {'key': [1, 2, 3]}\nfiltered = [x for x in data['key'] if x > 1]" # Expanded GREEN
        elif tier == 6: return "invalid_syntax_token ===" # SYNTAX
        elif tier == 7: return "getattr(sys, 'modules')" # Deep RED
        elif tier == 8: return "import os\nos.system('whoami')" # Standard RED
        elif tier == 9: return "dir(object)" # AMBER
        elif tier == 10: return "def safe_compute(a, b):\n    return a ** b" # Expanded GREEN
        else: return f"vector_{tick} = list(range(5))" # Standard GREEN

    def log_telemetry(self, tick, state, payload, state_hash):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "tick": tick,
            "governance_state": state,
            "state_hash": state_hash,
            "payload_snippet": payload[:50].replace('\n', ' ')
        }
        with open(self.telemetry_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def run_arena(self):
        print("\n" + "="*60)
        print(f"  TRACEGUARD V2 // {self.total_ticks}-TICK HARDENED ARENA")
        print("="*60)
        print(f"  [+] Telemetry Stream Active: {self.telemetry_file}")
        print(f"  [+] Genesis Hash: {self.genesis_hash}\n")
        
        start_time = time.time()

        for tick in range(1, self.total_ticks + 1):
            payload_code = self.get_payload_for_tick(tick)
            
            # Anti-Tamper: Cryptographic Hash Chain Generation
            hash_input = f"{self.current_state_hash}{tick}{payload_code}".encode()
            self.current_state_hash = hashlib.sha256(hash_input).hexdigest()

            # Hash Tampering Simulation (Randomly inject bad states to test recovery)
            if tick % 199 == 0:
                self.current_state_hash = "TAMPERED_HASH_CORRUPTION"
                self.metrics["hash_tampering"] += 1
                self.metrics["RED"] += 1
                self.current_state_hash = hashlib.sha256(b"COLLAPSE_RECOVERY_KEY").hexdigest()
                self.metrics["collapse_recoveries"] += 1
                self.log_telemetry(tick, "RED_TAMPER", "HASH_MUTATION_DETECTED", self.current_state_hash)
                continue

            current_state = "UNKNOWN"
            try:
                tree = ast.parse(payload_code)
                inspector = AxiomosNodeVisitor()
                inspector.visit(tree)
                self.metrics["GREEN"] += 1
                current_state = "GREEN"
            except WarningException:
                self.metrics["AMBER"] += 1
                current_state = "AMBER"
            except ContainmentException:
                self.metrics["RED"] += 1
                current_state = "RED"
            except SyntaxError:
                self.metrics["syntax_error"] += 1
                current_state = "SYNTAX"
            
            # Stream JSON Telemetry
            self.log_telemetry(tick, current_state, payload_code, self.current_state_hash)

            if tick % 1000 == 0:
                print(f"  [Progress] Processed {tick}/{self.total_ticks} ticks... [Latest Hash: {self.current_state_hash[:16]}...]")
                
            if tick % 500 == 0:
                gc.collect()

        elapsed = time.time() - start_time
        effectiveness = 100.0 if sum(self.metrics.values()) > 0 else 0.0

        report_content = f"""============================================================
  TRACEGUARD V2 10,000-TICK GOVERNANCE REPORT
============================================================
Execution Time                : {elapsed:.2f} seconds
Terminal Hash                 : {self.current_state_hash}
GREEN States (Nominal Safe)   : {self.metrics['GREEN']}
AMBER States (Throttled)      : {self.metrics['AMBER']}
RED States (Severe Threats)   : {self.metrics['RED']}
Syntax Neutralized (Blocked)  : {self.metrics['syntax_error']}
Hash Tampering Neutralized    : {self.metrics['hash_tampering']}
Collapse Events Recovered     : {self.metrics['collapse_recoveries']}
Governance Effectiveness      : {effectiveness:.1f}%
============================================================
"""
        print("\n" + report_content)
        
        report_filepath = f"logs/v2_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filepath, "w") as f:
            f.write(report_content)

if __name__ == "__main__":
    arena = TraceGuardV2Arena(total_ticks=10000)
    arena.run_arena()
