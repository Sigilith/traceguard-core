import re
import socket

def get_home_router_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Resolves outbound Wi-Fi route assigned by home router
        s.connect(("192.168.1.1", 80))
        lan_ip = s.getsockname()[0]
    except Exception:
        try:
            s.connect(("8.8.8.8", 80))
            lan_ip = s.getsockname()[0]
        except Exception:
            lan_ip = "127.0.0.1"
    finally:
        s.close()
    return lan_ip

lan_ip = get_home_router_ip()
print(f"[*] Discovered Home Router LAN IP: {lan_ip}")

# Inject IP resolution helper into sidecar
sidecar_path = "three_lineage_sidecar.py"
if True:
    with open(sidecar_path, "r") as f:
        content = f.read()

    binding_code = f"""
import socket
def get_router_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

HOST = get_router_ip()
"""
    # Prepend or inject the dynamic IP getter into sidecar configuration
    with open(".lineage/router_ip.env", "w") as env_f:
        env_f.write(f"ROUTER_LAN_IP={lan_ip}\n")
        
    print(f"[+] Saved router perimeter target to .lineage/router_ip.env ({lan_ip})")

