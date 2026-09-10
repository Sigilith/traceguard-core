import os, sys, time, socket
from http.server import HTTPServer, BaseHTTPRequestHandler

def get_router_ip():
    if os.path.exists(".lineage/router_ip.env"):
        with open(".lineage/router_ip.env") as f:
            for line in f:
                if "ROUTER_LAN_IP" in line:
                    return line.split("=")[1].strip()
    return "192.168.1.74"

HOST = get_router_ip()
PORT = 8443

class SidecarHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "active", "boundary": "router_bound"}\n')
    def log_message(self, format, *args):
        with open("sys_production.log", "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format%args}\n")

if __name__ == "__main__":
    print(f"[*] Starting Three-Lineage Sidecar bound to Router IP: {HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), SidecarHandler)
    server.serve_forever()
