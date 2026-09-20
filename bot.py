import os
import sys
import re
import json

def scan_code_vulnerabilities(target_dir):
    """Scans code directories for high-yield security vulnerabilities and secrets."""
    findings = []
    patterns = [
        (r'eval\(', 'Unsafe Dynamic Code Execution (eval)'),
        (r'exec\(', 'Unsafe Dynamic Code Execution (exec)'),
        (r'os\.system\(', 'Unsanitized Shell Command Execution'),
        (r'subprocess\.(run|Popen|call).*shell\s*=\s*True', 'Potential Command Injection via shell=True'),
        (r'pickle\.load', 'Insecure Deserialization (Pickle)'),
        (r'md5\(', 'Weak Cryptographic Hash (MD5)'),
        (r'api[_-]?key\s*=', 'Hardcoded API Key / Secret Exposure'),
        (r'password\s*=', 'Hardcoded Password Exposure'),
        (r'0\.0\.0\.0', 'Insecure Bind Address (All Interfaces)')
    ]
    
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(('.py', '.js', '.env', '.json', '.yml')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as sf:
                        for line_num, line in enumerate(sf, 1):
                            for pattern, desc in patterns:
                                if re.search(pattern, line, re.IGNORECASE):
                                    findings.append({
                                        "file": filepath,
                                        "line": line_num,
                                        "vector": desc
                                    })
                except Exception:
                    pass
    return findings

def run_revenue_pipeline(findings):
    import modules.client_reports.generator as cr
    import modules.bounty_vrt.formatter as bv
    print("[*] Generating Client Audit Report...")
    print(cr.generate_client_summary(findings))
    print("[*] Formatting HackerOne VRT Payload...")
    print(bv.format_vrt_payload(json.dumps({"vector_description": f"Found {len(findings)} risk vectors in target codebase"})))

if __name__ == "__main__":
    target_dir = "."
    if "--local" in sys.argv:
        try:
            idx = sys.argv.index("--local")
            target_dir = sys.argv[idx + 1]
        except IndexError:
            pass
            
    print(f"=======================================================================")
    print(f"🔍 TRACEGUARD MULTI-STREAM VULNERABILITY & REVENUE SCANNER")
    print(f"Target Directory: {target_dir}")
    print(f"=======================================================================")
    
    findings = scan_code_vulnerabilities(target_dir)
    print(f"[*] Vulnerability scan complete. Detected {len(findings)} potential risk vectors.")
    if findings:
        print("[+] Triggering Multi-Stream Revenue Pipeline...")
        run_revenue_pipeline(findings)
    else:
        print("[+] 🔒 Codebase clean of high-risk execution patterns.")
