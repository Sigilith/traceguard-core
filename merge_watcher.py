import os
import json
import urllib.request
import time

def check_open_prs():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("[-] No GITHUB_TOKEN found.")
        return

    print("[*] [Merge-Watcher] Polling active pull requests for merge status...")
    
    # We query PRs created by the user or containing 'traceguard-patch'
    url = "https://api.github.com/search/issues?q=author:Sigilith+type:pr+state:open"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TraceGuard-Merge-Watcher"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            items = data.get('items', [])
            print(f"[*] [Merge-Watcher] Monitoring {len(items)} active open pull requests.")
            for item in items:
                pr_url = item['html_url']
                title = item['title']
                repo = item['repository_url'].split('/')[-2] + '/' + item['repository_url'].split('/')[-1]
                print(f"  - [{repo}] {title} ({pr_url}) -> Status: OPEN")
    except Exception as e:
        print(f"[-] Merge-Watcher poll error: {e}")

if __name__ == "__main__":
    check_open_prs()
