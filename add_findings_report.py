with open("traceguard_engine.py", "r") as f:
    code = f.read()

# We will update autonomous_global_hunt to collect results and print a summary report at the end
old_hunt = '''def autonomous_global_hunt():
    processed_issues = get_already_processed_issues()
    print("[*] [Autonomous Agent] Activating intelligent global reward radar (Batch Limit: 70)...")

    query = urllib.parse.quote("bounty OR reward state:open label:bounty,bug")
    url = "https://api.github.com/search/issues?q=" + query + "&sort=updated&per_page=70"
    req = urllib.request.Request(url, headers={'User-Agent': 'TraceGuard-Autonomous-Agent'})

    try:
        with urllib.request.urlopen(req) as response:
            items = json.loads(response.read().decode()).get('items', [])
            print(f"[*] [Autonomous Agent] Discovered {len(items)} global candidates.")
            executed_count = 0
            for item in items:
                repo_slug = f"{item['repository_url'].split('/')[-2]}/{item['repository_url'].split('/')[-1]}"
                issue_num = str(item['number'])

                if issue_num in processed_issues:
                    continue

                process_target(repo_slug, issue_num, item['title'])
                executed_count += 1
                if executed_count >= 70:
                    print("\\n[*] [Autonomous Agent] Batch limit of 70 reached.")
                    break
    except Exception as e:
        print(f"[-] Global scan error: {e}")'''

new_hunt = '''def autonomous_global_hunt():
    processed_issues = get_already_processed_issues()
    print("[*] [Autonomous Agent] Activating intelligent global reward radar (Batch Limit: 70)...")

    query = urllib.parse.quote("bounty OR reward state:open label:bounty,bug")
    url = "https://api.github.com/search/issues?q=" + query + "&sort=updated&per_page=70"
    req = urllib.request.Request(url, headers={'User-Agent': 'TraceGuard-Autonomous-Agent'})

    run_findings = []

    try:
        with urllib.request.urlopen(req) as response:
            items = json.loads(response.read().decode()).get('items', [])
            print(f"[*] [Autonomous Agent] Discovered {len(items)} global candidates.")
            executed_count = 0
            for item in items:
                repo_slug = f"{item['repository_url'].split('/')[-2]}/{item['repository_url'].split('/')[-1]}"
                issue_num = str(item['number'])
                title = item['title']

                if issue_num in processed_issues:
                    continue

                status = process_target(repo_slug, issue_num, title)
                run_findings.append({
                    "repo": repo_slug,
                    "issue": issue_num,
                    "title": title,
                    "status": status
                })
                executed_count += 1
                if executed_count >= 70:
                    print("\\n[*] [Autonomous Agent] Batch limit of 70 reached.")
                    break

        # PRINT FINAL FINDINGS REPORT
        print("\\n" + "="*70)
        print("📊 TRACEGUARD HUNT FINDINGS & EXECUTION REPORT")
        print("="*70)
        if not run_findings:
            print("No new targets processed in this batch (all discovered issues were already in ledger).")
        else:
            for f in run_findings:
                print(f"• [{f['status']}] Repo: {f['repo']} | Issue #{f['issue']} — {f['title'][:50]}...")
        print("="*70)
        print(f"[+] Batch complete. Total targets processed this run: {len(run_findings)}")
        print("="*70)

    except Exception as e:
        print(f"[-] Global scan error: {e}")'''

# Also update process_target to return its status string so the findings list can capture it
old_process = '''        if push_res.returncode == 0:
            pr_url = create_github_pr(raw_repo, issue_id, branch_name, title, token)
            status = "PR Submitted" if pr_url else "Push Succeeded, PR Failed"
        else:
            status = "Push Failed"

        ledger_entry = f"| #{issue_id} | {raw_repo} | {status} | High-Scale Sweep | {datetime.now().strftime('%Y-%m-%d')} |\\n"
        with open("PAYMENT_LEDGER.md", "a") as f:
            f.write(ledger_entry)
        print(f"[+] [PaymentBot] Pipeline cycle complete for #{issue_id}.")
    except Exception as e:
        print(f"[-] [AXIOMOS] Execution failure: {e}")'''

new_process = '''        if push_res.returncode == 0:
            pr_url = create_github_pr(raw_repo, issue_id, branch_name, title, token)
            status = "PR Submitted" if pr_url else "Push Succeeded, PR Failed"
        else:
            status = "Push Failed"

        ledger_entry = f"| #{issue_id} | {raw_repo} | {status} | High-Scale Sweep | {datetime.now().strftime('%Y-%m-%d')} |\\n"
        with open("PAYMENT_LEDGER.md", "a") as f:
            f.write(ledger_entry)
        print(f"[+] [PaymentBot] Pipeline cycle complete for #{issue_id}.")
        return status
    except Exception as e:
        print(f"[-] [AXIOMOS] Execution failure: {e}")
        return "Error"'''

if old_hunt in code and old_process in code:
    code = code.replace(old_process, new_process).replace(old_hunt, new_hunt)
    with open("traceguard_engine.py", "w") as f:
        f.write(code)
    print("[+] Findings summary report added successfully!")
else:
    print("[-] Targeted code blocks not exact, check script structure.")

