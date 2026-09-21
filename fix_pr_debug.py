with open("bounty_pipeline.py", "r") as f:
    lines = f.readlines()

# Replace lines 113 to 119 with robust HTTPError capturing
new_try_block = [
    "    try:\n",
    "        with urllib.request.urlopen(req) as response:\n",
    "            res_data = json.loads(response.read().decode())\n",
    "            print(f\"[+] [PaymentBot] Pull request successfully opened! URL: {res_data.get('html_url')}\")\n",
    "            return res_data.get('html_url')\n",
    "    except urllib.error.HTTPError as he:\n",
    "        error_body = he.read().decode()\n",
    "        print(f\"[-] [PaymentBot] Failed to create pull request via API (HTTP {he.code}): {error_body}\")\n",
    "    except Exception as e:\n",
    "        print(f\"[-] [PaymentBot] Failed to create pull request via API: {e}\")\n"
]

# Find where 'try:' starts in create_github_pr
for i, line in enumerate(lines):
    if 'def create_github_pr' in line:
        for j in range(i, len(lines)):
            if lines[j].strip() == "try:":
                # Replace from try: to the end of the function
                lines[j:j+7] = new_try_block
                break
        break

with open("bounty_pipeline.py", "w") as f:
    f.writelines(lines)

print("[+] Detailed error logging installed successfully!")
