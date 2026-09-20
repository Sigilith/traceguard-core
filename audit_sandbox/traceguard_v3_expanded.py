import sys, time, gc, ast, datetime, hashlib, json

class ContainmentException(Exception): pass
class WarningException(Exception): pass

class AxiomosExpandedVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nesting_depth = 0

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in ['subprocess', 'os', 'socket', 'urllib', 'requests', 'sys', 'ctypes', 'pickle', 'importlib']:
                raise ContainmentException()
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr in ['__builtins__', '__dict__', '__class__', '__subclasses__', '_getframe']:
            raise ContainmentException()
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            # Expanded RED
            if node.func.id in ['exec', 'eval', 'open', '__import__', 'compile']:
                raise ContainmentException()
            # Expanded AMBER
            if node.func.id in ['globals', 'locals', 'vars', 'dir', 'setattr', 'getattr', 'hasattr', 'type']:
                raise WarningException()
        self.generic_visit(node)

    def visit_For(self, node):
        self.nesting_depth += 1
        if self.nesting_depth > 3: raise WarningException()
        self.generic_visit(node)
        self.nesting_depth -= 1
        
    def visit_While(self, node):
        raise WarningException() # Throttle unbounded loops

class TraceGuardV3Arena:
    def __init__(self, total_ticks=5000):
        self.total_ticks = total_ticks
        self.genesis_hash = hashlib.sha256(b"TRACEGUARD_V3_EXPANDED").hexdigest()
        self.current_hash = self.genesis_hash
        self.telemetry_file = f"logs/telemetry/run_v3_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

    def get_payload(self, tick):
        tier = tick % 14
        # RED
        if tier == 0: return "import pickle\npickle.loads(b'')"
        elif tier == 1: return "import importlib\nimportlib.import_module('os')"
        elif tier == 2: return "sys._getframe(0)"
        # AMBER
        elif tier == 3: return "while True:\n  pass"
        elif tier == 4: return "hasattr(obj, 'private_key')"
        elif tier == 5: return "type(unknown_obj)()"
        # GREEN (Expanded Safe Library)
        elif tier == 6: return "from collections import defaultdict\nd = defaultdict(int)"
        elif tier == 7: return "import itertools\nlist(itertools.islice(range(10), 5))"
        elif tier == 8: return "text = 'traceguard'.upper()[::-1]"
        elif tier == 9: return "def calc_variance(data):\n  return sum(data)/len(data)"
        else: return "import os\nos.system('id')" # Baseline RED

    def log_telemetry(self, tick, state, payload, state_hash):
        log_entry = {"timestamp": datetime.datetime.now().isoformat(), "tick": tick, "state": state, "hash": state_hash, "payload": payload[:40]}
        with open(self.telemetry_file, "a") as f: f.write(json.dumps(log_entry) + "\n")

    def run(self):
        print(f"\n[+] Executing V3 Expanded Arena (5,000 ticks) -> {self.telemetry_file}")
        for tick in range(1, self.total_ticks + 1):
            payload = self.get_payload(tick)
            self.current_hash = hashlib.sha256(f"{self.current_hash}{tick}{payload}".encode()).hexdigest()
            
            state = "UNKNOWN"
            try:
                ast.parse(payload)
                visitor = AxiomosExpandedVisitor()
                visitor.visit(ast.parse(payload))
                state = "GREEN"
            except WarningException: state = "AMBER"
            except ContainmentException: state = "RED"
            except SyntaxError: state = "SYNTAX"
            
            self.log_telemetry(tick, state, payload, self.current_hash)
            if tick % 1000 == 0: gc.collect()
        print("[+] V3 Execution Complete. Telemetry written.\n")

if __name__ == "__main__":
    TraceGuardV3Arena().run()
