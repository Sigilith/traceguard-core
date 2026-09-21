with open("traceguard_engine.py", "r") as f:
    code = f.read()

# Replace create_github_pr to handle 422 / existing PR errors gracefully
old_pr_func = '''def create_github_pr(repo_slug, issue_id, branch_name, patch_title, token):
    url = "https://api.github.com/repos/" + repo_slug + "/pulls"
    head_ref = f"Sigilith:{branch_name}"
    
    payload = {
        "title": f"Fix #{issue_id}: Automated AST Governed Patch for {patch_title}",
        "body": f"Automated solution generated via TraceGuard sovereign execution engine addressing issue #{issue_id}. Verified by ThreeLineage.",
        "head": head_ref,
        "base": "main"
    }

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "User-Agent": "TraceGuard-Autonomous-Agent"
        }, method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"[+] [PaymentBot] PR successfully opened! URL: {res_data.get('html_url')}")
            return res_data.get('html_url')
    except Exception as e:
        print(f"[-] [PaymentBot] Failed to create PR: {e}")
        return None'''

new_pr_func = '''def create_github_pr(repo_slug, issue_id, branch_name, patch_title, token):
    url = "https://api.github.com/repos/" + repo_slug + "/pulls"
    head_ref = f"Sigilith:{branch_name}"
    
    payload = {
        "title": f"Fix #{issue_id}: Automated AST Governed Patch for {patch_title}",
        "body": f"Automated solution generated via TraceGuard sovereign execution engine addressing issue #{issue_id}. Verified by ThreeLineage.",
        "head": head_ref,
        "base": "main"
    }

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "User-Agent": "TraceGuard-Autonomous-Agent"
        }, method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"[+] [PaymentBot] PR successfully opened! URL: {res_data.get('html_url')}")
            return res_data.get('html_url')
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        if "a pull request already exists" in err_body.lower():
            print(f"[!] [PaymentBot] PR already exists for issue #{issue_id}. Treating as success.")
            return "EXISTS"
        else:
            print(f"[-] [PaymentBot] Failed to create PR (HTTP {e.code}): {err_body}")
            return None
    except Exception as e:
        print(f"[-] [PaymentBot] Failed to create PR: {e}")
        return None'''

# Also update process_target to record "PR Already Exists" correctly
old_process_check = '''        if push_res.returncode == 0:
            pr_url = create_github_pr(raw_repo, issue_id, branch_name, title, token)
            status = "PR Submitted" if pr_url else "Push Succeeded, PR Failed"
        else:
            status = "Push Failed"'''

new_process_check = '''        if push_res.returncode == 0:
            pr_url = create_github_pr(raw_repo, issue_id, branch_name, title, token)
            if pr_url == "EXISTS":
                status = "PR Already Exists"
            elif pr_url:
                status = "PR Submitted"
            else:
                status = "Push Succeeded, PR Failed"
        else:
            status = "Push Failed"'''

if old_pr_func in code and old_process_check in code:
    code = code.replace(old_pr_func, new_pr_func).replace(old_process_check, new_process_check)
    with open("traceguard_engine.py", "w") as f:
        f.write(code)
    print("[+] Existing PR handling added successfully!")
else:
    print("[-] Exact match not found, check script structure.")

