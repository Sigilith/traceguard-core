with open("traceguard_engine.py", "r") as f:
    code = f.read()

# Fix malformed URL definition in autonomous_global_hunt
old_url = 'url = f"https://api.github.com/search/issues?q={query}&sort=updated&per_page=70"'
# Ensure it's cleanly assigned without bracket leaks
new_url = 'url = "https://api.github.com/search/issues?q=" + query + "&sort=updated&per_page=70"'

code = code.replace(old_url, new_url)

with open("traceguard_engine.py", "w") as f:
    f.write(code)

print("[+] URL parsing fixed!")
