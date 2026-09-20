import os
import re
import ast

# Regex patterns for high-value sensitive secrets & structural risks
SECRET_PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Stripe Live Key": re.compile(r"rk_live_[0-9a-zA-Z]{24}"),
    "Generic Private Key": re.compile(r"-----BEGIN PRIVATE KEY-----"),
    "Slack Token": re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}"),
    "GitHub Token": re.compile(r"ghp_[0-9a-zA-Z]{36}"),
}

def sniff_repository_files(target_dir):
    """Sniffs extracted repository files for exposed secrets and dynamic runtime risks."""
    sniffer_findings = []
    
    for root_dir, dirs, files in os.walk(target_dir):
        # Skip hidden git folders or virtual envs
        if ".git" in root_dir or "venv" in root_dir:
            continue
            
        for file in files:
            file_path = os.path.join(root_dir, file)
            rel_path = os.path.relpath(file_path, target_dir)
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                    # 1. Sniff for hardcoded secrets/tokens
                    for secret_name, pattern in SECRET_PATTERNS.items():
                        matches = pattern.findall(content)
                        if matches:
                            sniffer_findings.append({
                                "file": rel_path,
                                "line": 0,  # General file match
                                "vector": f"Exposed Credential / Secret ({secret_name})"
                            })
                            
                    # 2. Sniff Python files via AST for hidden dynamic execution
                    if file.endswith(".py"):
                        try:
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Call):
                                    if isinstance(node.func, ast.Name) and node.func.id in ["eval", "exec"]:
                                        sniffer_findings.append({
                                            "file": rel_path,
                                            "line": node.lineno,
                                            "vector": f"Sniffer Alert: Dynamic Code Execution ({node.func.id})"
                                        })
                        except Exception:
                            pass
            except Exception:
                pass
                
    return sniffer_findings
