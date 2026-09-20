import json
import urllib.request

WEBHOOK_URL = "https://discord.com/api/webhooks/1551227623001161869/0G2n9qtLzDrBy8eF6O6x62Ckxcg-rK0osrZMcBFQ8IURB8UG4iXN8_dE5B0z4cPhO-aC"

def send_alert(new_assets):
    if not new_assets:
        return

    message = f"🚨 **{len(new_assets)} New Asset(s) Detected!**\n"
    for asset in new_assets:
        message += f"• {asset}\n"

    payload = {"content": message}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        WEBHOOK_URL, 
        data=data, 
        headers={"Content-Type": "application/json", "User-Agent": "TraceGuard-Pipeline"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            print(f"[+] Alert dispatched successfully (Status: {response.status})")
    except Exception as e:
        print(f"[-] Failed to send alert: {e}")

if __name__ == "__main__":
    sample_assets = ["https://webhook-migration-test.santos.com"]
    send_alert(sample_assets)
