import json

def generate_client_summary(findings_list):
    """Generates an executive-ready Markdown summary for security clients."""
    total = len(findings_list)
    report = f"# TraceGuard Codebase Security Report\n\n"
    report += f"**Total Findings:** {total}\n"
    report += f"**Status:** {'PASSED' if total == 0 else 'ACTION REQUIRED'}\n\n"
    report += "## Risk Findings Detail\n"
    for item in findings_list:
        report += f"- **File:** `{item.get('file')}` (Line {item.get('line')})\n"
        report += f"  - **Type:** {item.get('vector')}\n"
    return report
