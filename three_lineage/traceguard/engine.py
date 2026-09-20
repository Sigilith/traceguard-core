import functools
import re
from typing import Dict, Any

class OptimizedTraceGuard:
    __slots__ = ('_forbidden_patterns', '_compiled_regex')

    def __init__(self):
        self._forbidden_patterns = ["os.system", "subprocess", "eval", "exec", "__import__"]
        self._compiled_regex = re.compile("|".join(map(re.escape, self._forbidden_patterns)))

    @functools.lru_cache(maxsize=1024)
    def inspect_cached(self, action_text: str) -> tuple:
        match = self._compiled_regex.search(action_text)
        safe = match is None
        risk = 0.0 if safe else 1.0
        return safe, risk

    def inspect(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        text = observation.get("action_text", "")
        safe, risk = self.inspect_cached(text)
        return {
            "ast_safe": safe,
            "risk_score": risk,
            "details": "Perimeter clean" if safe else "Forbidden pattern intercepted"
        }
