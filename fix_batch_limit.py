with open("bounty_pipeline.py", "r") as f:
    code = f.read()

import re

# Look for batch limit patterns like batch_limit = 5, limit = 5, or [:5] slicing
updated = False

# Try replacing explicit batch limit assignments
for pattern in [r'batch_limit\s*=\s*\d+', r'LIMIT\s*=\s*\d+', r'max_batch\s*=\s*\d+']:
    if re.search(pattern, code):
        code = re.sub(pattern, 'batch_limit = 20', code)
        updated = True

# Try replacing list slicing limits like [:5] or [:limit]
if not updated:
    # Look for candidate slices
    code = re.sub(r'candidates\s*=\s*candidates\[:\d+\]', 'candidates = candidates[:20]', code)
    code = re.sub(r'[:5]', '[:20]', code)

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Batch limit successfully increased to 20!")
