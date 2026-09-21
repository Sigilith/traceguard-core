with open("traceguard_engine.py", "r") as f:
    code = f.read()

# Replace the lenient get_already_processed_issues function with a strict success-only filter
old_func = '''def get_already_processed_issues():
    processed = set()
    ledger_file = "PAYMENT_LEDGER.md"
    if os.path.exists(ledger_file):
        with open(ledger_file, "r") as f:
            for line in f:
                if line.strip().startswith("| #"):
                    parts = line.split("|")
                    if len(parts) > 1:
                        issue_str = parts[1].strip().replace("#", "")
                        if issue_str.isdigit():
                            processed.add(issue_str)
    return processed'''

new_func = '''def get_already_processed_issues():
    processed = set()
    ledger_file = "PAYMENT_LEDGER.md"
    if os.path.exists(ledger_file):
        with open(ledger_file, "r") as f:
            for line in f:
                if line.strip().startswith("| #"):
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 4:
                        issue_str = parts[1].replace("#", "")
                        status = parts[3]
                        # ONLY skip if it successfully pushed or opened a PR. 
                        # Retry automatically if it failed previously ("Push Failed", etc.)
                        if issue_str.isdigit() and ("PR" in status or "Claimed" in status or "Submitted" in status):
                            processed.add(issue_str)
    return processed'''

code = code.replace(old_func, new_func)

with open("traceguard_engine.py", "w") as f:
    f.write(code)

print("[+] Duplicate avoidance upgraded: Agent will now skip confirmed successes and auto-retry past failures!")
