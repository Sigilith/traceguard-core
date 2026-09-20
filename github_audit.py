import requests

GITHUB_TOKEN = "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"
REPO_OWNER = "Sigilith"
REPO_NAME = "traceguard-core"

def audit_github_boundary():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
    
    print(f"[*] Initiating structural audit for: {REPO_OWNER}/{REPO_NAME}")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repo_data = response.json()
        if repo_data.get("private"):
            print("[+] PASS: Repository visibility is restricted (Private).")
        else:
            print("[-] FAIL: Repository is PUBLIC. Intellectual property is exposed.")
    elif response.status_code == 404:
        print("[-] FAIL: Repository not found. Ensure the repo exists and your token has 'repo' scope.")
    else:
        print(f"[-] ERROR: Failed to connect to GitHub API (Status: {response.status_code})")

if __name__ == "__main__":
    audit_github_boundary()
