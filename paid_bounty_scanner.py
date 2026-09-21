import urllib.request
import json
import subprocess
import os
import urllib.parse

def get_already_processed_issues():
    processed = set()
    ledger_file = "PAYMENT_LEDGER.md"
    if os.path.exists(ledger_file):
        with open(ledger_file, "r") as f:
            for line in f:
                if line.strip().startswith("| #"):
                    parts = line.split("|")
                    if len(parts) > 1:
                        issue_str = parts[1].strip().replace("#", "")
                        if issue_str.isdigit():
                            processed.add(issue_str)
    return processed

def autonomous_global_hunt():
    processed_issues = get_already_processed_issues()
    print("[*] [Autonomous Agent] Activating global reward radar across worldwide repositories...")
    
    # Search globally on GitHub for open issues containing bounty, reward, or sponsor keywords
    query = urllib.parse.quote("bounty OR reward OR sponsor state:open label:bounty,good first issue,help wanted")
    url = f"https://api.github.com/search/issues?q={query}&sort=updated&per_page=10"
    
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'TraceGuard-Autonomous-Agent', 
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('items', [])
            print(f"[*] [Autonomous Agent] Discovered {len(items)} global reward/fix candidates.")
            
            executed_count = 0
            for item in items:
                title = item['title']
                issue_url = item['html_url']
                # Extract repo slug from URL (e.g., https://github.com/owner/repo/issues/123 -> owner/repo)
                parts = item['repository_url'].split('/')
                repo_slug = f"{parts[-2]}/{parts[-1]}"
                issue_num = str(item['number'])
                
                # Deduplicate based on ledger
                composite_id = f"{repo_slug}#{issue_num}"
                if issue_num in processed_issues:
                    continue
                    
                print(f"\n[+] [Target Acquired] Repo: {repo_slug} | Issue #{issue_num}: {title}")
                print(f"    [!] Autonomous decision: High potential reward detected. Initiating AXIOMOS containment...")
                
                # Trigger governed pipeline
                result = subprocess.run(["python3", "governed_bounty.py", repo_slug, issue_num])
                if result.returncode == 0:
                    executed_count += 1
                    
                # Limit to top autonomous picks per run to manage rate limits
                if executed_count >= 3:
                    print("\n[*] [Autonomous Agent] Batch limit reached. Pausing to review ledger and sandbox outputs.")
                    break
                    
            if executed_count == 0:
                print("[+] All discovered global targets are already logged or processed.")
    except Exception as e:
        print(f"[-] Global scan error: {e}")

if __name__ == "__main__":
    autonomous_global_hunt()
