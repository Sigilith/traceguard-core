import json

def format_vrt_payload(scan_results_json):
    """Maps internal AST risk vectors to Bugcrowd VRT and Priority ratings (P1-P5)."""
    data = json.loads(scan_results_json)
    severity = data.get("severity", "Medium").lower()
    
    # Map severity to Bugcrowd Priority
    priority_map = {
        "critical": "P1 (Critical)",
        "high": "P2 (High)",
        "medium": "P3 (Medium)",
        "low": "P4 (Low)",
        "informational": "P5 (Informational)"
    }
    priority = priority_map.get(severity, "P3 (Medium)")

    vrt_payload = {
        "submission_title": f"[TraceGuard] {data.get('vector_description', 'AST Vulnerability Vector')}",
        "vulnerability_information": data.get("vector_description", "Unverified AST risk vector"),
        "bugcrowd_priority": priority,
        "vrt_category": "Server-Side Execution / Code Quality",
        "impact": "Potential security boundary violation or unauthorized execution path."
    }
    return json.dumps(vrt_payload, indent=2)
