import re

with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Clean replacement for the entire elyan JSON block
new_elyan_block = '''    elif "elyan" in title_lower or "rustchain" in title_lower or "rtc" in title_lower:
        target_file = os.path.join(sandbox_dir, f"submissions/judge-packets/response_{issue_id}.json")
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        content = json.dumps({
            "issue_id": issue_id,
            "respondent": "TraceGuard Autonomous Agent",
            "statement": "Choosing to work on Elyan Labs/Rustchain repos because of their focus on sovereign execution and verifiable decentralized protocols."
        }, indent=2)'''

# Replace from 'elif "elyan"' up to the next 'else:'
pattern = r'elif "elyan".*?(?=\n\s*else:)'
if re.search(pattern, code, re.DOTALL):
    code = re.sub(pattern, new_elyan_block, code, flags=re.DOTALL)
    with open("bounty_pipeline.py", "w") as f:
        f.write(code)
    print("[+] Elyan block cleanly rewritten!")
else:
    print("[-] Pattern not found, manual check needed.")
