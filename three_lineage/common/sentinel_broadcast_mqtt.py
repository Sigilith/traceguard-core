import time
from pathlib import Path
import paho.mqtt.client as mqtt

RECEIPTS_DIR = Path(".lineage/derek_receipts")
POLL_INTERVAL = 2
BROKER = "localhost"
PORT = 1883
TOPIC = "threelineage/mesh/containment"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[+] Derek linked to Local Mesh: {BROKER}")
    else:
        print(f"[-] Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    print(f"[+] Receipt broadcasted successfully: {TOPIC}")

def start_mqtt_daemon():
    print("[*] Starting Sentinel Mesh MQTT Broadcast Daemon...")
    if not RECEIPTS_DIR.exists():
        RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)

    client = mqtt.Client(client_id="derek_node_alpha")
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"[CRITICAL] Could not connect: {e}")
        return

    processed = {f.name for f in RECEIPTS_DIR.glob("*.json")}
    print(f"[*] Found {len(processed)} existing receipts. Monitoring queue...")

    try:
        while True:
            current_files = {f.name for f in RECEIPTS_DIR.glob("*.json")}
            new_files = current_files - processed
            for file_name in new_files:
                print(f"\n[!] New receipt detected: {file_name}")
                client.publish(TOPIC, (RECEIPTS_DIR / file_name).read_text(), qos=1)
                processed.add(file_name)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\n[*] Daemon halted.")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    start_mqtt_daemon()
