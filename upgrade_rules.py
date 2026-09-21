with open("bot.py", "r") as f:
    code = f.read()

# Expanded ruleset for broader vulnerability detection
new_rules = """
def scan_code_vulnerabilities(target_dir):
    import os
    findings = []
    patterns = [
        (r'eval\\(', 'Unsafe Dynamic Code Execution (eval)'),
        (r'exec\\(', 'Unsafe Dynamic Code Execution (exec)'),
        (r'os\\.system\\(', 'Unsanitized Shell Command Execution'),
        (r'subprocess\\.(run|Popen|call).*shell\\s*=\\s*True', 'Potential Command Injection via shell=True'),
        (r'pickle\\.load', 'Insecure Deserialization (Pickle)'),
        (r'md5\\(', 'Weak Cryptographic Hash (MD5)'),
        (r'api[_-]?key\\s*=', 'Hardcoded API Key / Secret Exposure'),
        (r'password\\s*=', 'Hardcoded Password Exposure'),
        (r'0\\.0\\.0\\.0', 'Insecure Bind Address (All Interfaces)')
    ]
    
    for root, dirs, files in os.walk(target_dir):
        # Skip hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(('.py', '.js', '.env', '.json', '.yml')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as sf:
                        for line_num, line in enumerate(sf, 1):
                            for pattern, desc in patterns:
                                import re
                                if re.search(pattern, line, re.IGNORECASE):
                                    findings.append({
                                        "file": filepath,
                                        "line": line_num,
                                        "vector": desc
                                    })
                except Exception:
                    pass
    return findings
"""

# Replace the old scan_code_vulnerabilities function with the expanded one
if "def scan_code_vulnerabilities" in code:
    parts = code.split("def scan_code_vulnerabilities")
    prefix = parts[0]
    # Find where the function ends (next def or main block)
    remainder = parts[1]
    if "if __name__ == "__main__":" in remainder:
        suffix = "if __name__ == "__main__":" + remainder.split("if __name__ == "__main__":")[1]
    else:
        suffix = ""
    updated_code = prefix + new_rules + "\n" + suffix
    with open("bot.py", "w") as f:
        f.write(updated_code)
    print("Bot vulnerability ruleset successfully expanded!")
else:
    print("Could not locate scan_code_vulnerabilities function.")
