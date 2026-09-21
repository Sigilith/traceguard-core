with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Fix the specific uncoloned dictionary pair on line 74
code = code.replace('"respondent" "TraceGuard Autonomous Agent"', '"respondent": "TraceGuard Autonomous Agent"')

# General regex for any other "key" "value" or "key" variable missing a colon in dicts
import re
code = re.sub(r'(\s*["\'][a-zA-Z_0-9]+["\'])\s+([a-zA-Z_0-9"\'-]+)\s*,', r'\1: \2,', code)

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Line 74 dictionary syntax fixed!")
