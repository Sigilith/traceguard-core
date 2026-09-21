with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Fix uncoloned dictionary key-value pairs
code = code.replace('"issue_id" issue_id', '"issue_id": issue_id')
code = code.replace('"repo_slug" repo_slug', '"repo_slug": repo_slug')
code = code.replace('"status" status', '"status": status')
code = code.replace('"title" title', '"title": title')

import re
# General regex fallback for any remaining `"key" value` patterns in dicts
code = re.sub(r'(\s*["\'][a-zA-Z_]+["\'])\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*,', r'\1: \2,', code)

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Dictionary syntax fixed successfully!")
