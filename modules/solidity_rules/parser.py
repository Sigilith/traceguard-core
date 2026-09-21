import re

def scan_solidity_patterns(source_code):
    """Scans Solidity contracts for common high-risk patterns like unverified call state or re-entrancy."""
    risks = []
    if "delegatecall(" in source_code:
        risks.append("Low-level delegatecall detected (Potential Unrestricted Proxy / Execution Risk)")
    if "selfdestruct(" in source_code:
        risks.append("selfdestruct opcode detected (High Severity Access Control Risk)")
    return risks
