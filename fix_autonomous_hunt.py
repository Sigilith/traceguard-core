with open("bounty_pipeline.py", "r") as f:
    code = f.read()

# Fix the broken URL, missing per_page value, and missing header colons
old_req_block = '''    query = urllib.parse.quote("bounty OR reward OR sponsor stateopen labelbounty,good first issue,help wanted")
    url = f"https//api.github.com/search/issues?q={query}&sort=updated&per_page="
             
    req = urllib.request.Request(url, headers={'User-Agent' 'TraceGuard-Autonomous-Agent', 'Accept' 'application/vnd.github.v3+json'})'''

new_req_block = '''    query = urllib.parse.quote("bounty OR reward OR sponsor state:open label:bounty,good first issue,help wanted")
    url = f"https://api.github.com/search/issues?q={query}&sort=updated&per_page=20"
             
    req = urllib.request.Request(url, headers={
        'User-Agent': 'TraceGuard-Autonomous-Agent',
        'Accept': 'application/vnd.github.v3+json'
    })'''

old_limit = 'if executed_count >= 2:'
new_limit = 'if executed_count >= 20:'

code = code.replace(old_req_block, new_req_block)
code = code.replace(old_limit, new_limit)

with open("bounty_pipeline.py", "w") as f:
    f.write(code)

print("[+] Autonomous hunt function patched successfully!")
