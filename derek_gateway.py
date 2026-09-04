from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path

INBOUND_DIR = Path(".lineage/inbound_work")
PORT = 8080

class TaskWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            task_data = json.loads(post_data.decode('utf-8'))
            INBOUND_DIR.mkdir(parents=True, exist_ok=True)
            
            task_id = task_data.get("task_id", "task_" + Path(self.path).name or "incoming")
            task_file = INBOUND_DIR / f"{task_id}.json"
            task_file.write_text(json.dumps(task_data, indent=2))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "received", "queued_file": task_file.name}).encode())
            print(f"[+] Inbound task captured via Webhook and queued: {task_file.name}")
            
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            print(f"[-] Webhook error: {e}")

def run_server():
    INBOUND_DIR.mkdir(parents=True, exist_ok=True)
    server = HTTPServer(('0.0.0.0', PORT), TaskWebhookHandler)
    print(f"[*] Derek Webhook Gateway active on port {PORT}...")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
