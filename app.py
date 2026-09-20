from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import tempfile
import os
import ast
import urllib.request
import zipfile
import json
from sniffer import sniff_repository_files

app = FastAPI(title="TraceGuard Enterprise Sniffer", version="4.5")

PAID_SESSIONS = {"DEMO_PAID_TOKEN_123"}
AUDIT_LOG_FILE = "corporate_audit_log.json"

def get_leaderboard_data():
    if os.path.exists(AUDIT_LOG_FILE):
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"scan_batch_count": 0, "total_risks_detected": 0, "results": []}
    return {"scan_batch_count": 0, "total_risks_detected": 0, "results": []}

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def root():
    data = get_leaderboard_data()
    total_scanned = data.get("scan_batch_count", 0)
    total_risks = data.get("total_risks_detected", 0)
    results = data.get("results", [])

    rows_html = ""
    for r in results:
        repo = r.get("repository", "Unknown")
        risks = r.get("total_containment_risks_detected", 0)
        badge_color = "#ef4444" if risks > 0 else "#22c55e"
        rows_html += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #334155;">{repo}</td>
            <td style="padding: 12px; border-bottom: 1px solid #334155; text-align: center;"><span style="background: {badge_color}; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{risks}</span></td>
            <td style="padding: 12px; border-bottom: 1px solid #334155; text-align: center;">{r.get('status', 'LOCKED')}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TraceGuard Sniffer Portal</title>
        <style>
            body {{ background-color: #0f172a; color: #f8fafc; font-family: sans-serif; margin: 0; padding: 40px; display: flex; flex-direction: column; align-items: center; }}
            .container {{ width: 800px; max-width: 100%; }}
            .header {{ background-color: #1e293b; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 30px; }}
            .stats-box {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-card {{ background: #0f172a; padding: 15px 25px; border-radius: 8px; border: 1px solid #334155; }}
            .stat-number {{ font-size: 24px; font-weight: bold; color: #3b82f6; }}
            table {{ width: 100%; border-collapse: collapse; background-color: #1e293b; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
            th {{ background-color: #334155; padding: 14px; text-align: left; font-size: 14px; }}
            input, button {{ width: 100%; padding: 12px; margin: 10px 0; border-radius: 5px; border: 1px solid #334155; background: #0f172a; color: white; font-size: 16px; box-sizing: border-box; }}
            button {{ background-color: #3b82f6; font-weight: bold; cursor: pointer; border: none; }}
            button:hover {{ background-color: #60a5fa; }}
            .scan-box {{ background-color: #1e293b; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>🛡️ TraceGuard Sniffer Engine</h2>
                <p>AST + Secret & Vulnerability Sniffing Dashboard</p>
                <div class="stats-box">
                    <div class="stat-card">
                        <div>Total Audited</div>
                        <div class="stat-number">{total_scanned}</div>
                    </div>
                    <div class="stat-card">
                        <div>Risks Flagged</div>
                        <div class="stat-number">{total_risks}</div>
                    </div>
                </div>
            </div>

            <div class="scan-box">
                <h3>Run Repository Sniffer Scan</h3>
                <form action="/scan-git" method="post">
                    <input type="url" name="github_url" placeholder="https://github.com/username/repository" required>
                    <input type="password" name="github_token" placeholder="Optional: GitHub Token (for Private Repos)">
                    <input type="text" name="payment_token" placeholder="Payment Token (To Unlock Report)">
                    <button type="submit">Run Sniffer Audit</button>
                </form>
            </div>

            <h3>Threat Intelligence Leaderboard</h3>
            <table>
                <thead>
                    <tr>
                        <th>Repository Target</th>
                        <th style="text-align: center;">Containment Risks</th>
                        <th style="text-align: center;">Audit Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html if rows_html else '<tr><td colspan="3" style="padding: 20px; text-align: center;">No audit logs found.</td></tr>'}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

@app.get("/pay")
async def pay():
    return RedirectResponse(url="https://buy.stripe.com/00wcN4df1bVb2xP7Cx3sI00")

@app.post("/webhook")
async def stripe_webhook(request: Request):
    try:
        body = await request.json()
        if body.get("type") == "checkout.session.completed":
            session = body.get("data", {}).get("object", {})
            session_id = session.get("id")
            if session_id:
                PAID_SESSIONS.add(session_id)
        return {"status": "success"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/scan-git")
async def scan_git(github_url: str = Form(...), github_token: str = Form(None), payment_token: str = Form(None)):
    clean_url = github_url.rstrip("/")
    if clean_url.endswith(".git"):
        clean_url = clean_url[:-4]
    
    branches = ["main", "master"]
    downloaded = False
    
    headers = {'User-Agent': 'TraceGuard-Sniffer-Scanner'}
    if github_token:
        headers['Authorization'] = f"token {github_token}"
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = os.path.join(tmp_dir, "repo.zip")
        last_error = ""
        
        for branch in branches:
            zip_url = f"{clean_url}/archive/refs/heads/{branch}.zip"
            try:
                req = urllib.request.Request(zip_url, headers=headers)
                with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
                    out_file.write(response.read())
                downloaded = True
                break
            except Exception as e:
                last_error = str(e)
                continue
        
        if not downloaded:
            return {"error": f"Failed to download repository. Details: {last_error}"}
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmp_dir)
            
            risks_detail = []
            py_files_count = 0
            
            for root_dir, dirs, files in os.walk(tmp_dir):
                for file in files:
                    if file.endswith(".py"):
                        py_files_count += 1
                        file_path = os.path.join(root_dir, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                tree = ast.parse(f.read())
                                rel_path = os.path.relpath(file_path, tmp_dir)
                                
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.Call):
                                        if isinstance(node.func, ast.Name):
                                            if node.func.id in ["eval", "exec", "__import__"]:
                                                risks_detail.append({"file": rel_path, "line": node.lineno, "vector": f"Dangerous Built-in ({node.func.id})"})
                                        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                                            mod = node.func.value.id
                                            attr = node.func.attr
                                            if mod == "os" and attr in ["system", "popen", "spawn"]:
                                                risks_detail.append({"file": rel_path, "line": node.lineno, "vector": f"OS Command Execution (os.{attr})"})
                                            elif mod == "subprocess" and attr in ["run", "Popen", "call", "check_output"]:
                                                risks_detail.append({"file": rel_path, "line": node.lineno, "vector": f"Subprocess Execution (subprocess.{attr})"})
                                            elif mod == "pickle" and attr in ["load", "loads"]:
                                                risks_detail.append({"file": rel_path, "line": node.lineno, "vector": f"Unsafe Deserialization (pickle.{attr})"})
                        except Exception:
                            pass
            
            sniffer_results = sniff_repository_files(tmp_dir)
            risks_detail.extend(sniffer_results)
            
            is_paid = payment_token in PAID_SESSIONS
            
            if is_paid:
                return {
                    "repository": github_url,
                    "python_files_scanned": py_files_count,
                    "status": "UNLOCKED",
                    "total_containment_risks_detected": len(risks_detail),
                    "full_remediation_patch": risks_detail
                }
            else:
                return {
                    "repository": github_url,
                    "python_files_scanned": py_files_count,
                    "status": "LOCKED",
                    "total_containment_risks_detected": len(risks_detail),
                    "message": "Audit report locked. Pay £49.99 via Stripe to unlock full remediation patch.",
                    "payment_link": "/pay",
                    "preview_risks": risks_detail[:2]
                }
        except Exception as e:
            return {"error": f"Failed to parse repository files. Details: {str(e)}"}
