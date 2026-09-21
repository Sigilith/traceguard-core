import subprocess
import requests

def fetch_and_contain_all():
    print("[*] Fetching all active global bounties...")
    search_url = "https://api.github.com/search/issues?q=is:open+is:issue+label:bounty&sort=created&order=desc&per_page=5"
    response = requests.get(search_url, headers={"Accept": "application/vnd.github.v3+json"})
    
    if response.status_code != 200:
        print(f"[-] Failed to fetch bounties: {response.status_code}")
        return

    items = response.json().get("items", [])
    for issue in items:
        repo_url = issue['repository_url'].replace("api.github.com/repos", "github.com") + ".git"
        issue_id = issue['number']
        title = issue['title']
        
        print(f"\n[!] Processing Bounty: {title}")
        print(f"    Target Repo: {repo_url}")
        
        # Hand off to the AXIOMOS governance engine sandbox
        subprocess.run(["python3", "governed_bounty.py", repo_url, str(issue_id)])

if __name__ == "__main__":
    fetch_and_contain_all()
