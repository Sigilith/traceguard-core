import json
import urllib.request

WEBHOOK_URL = "https://discord.com/api/webhooks/1551198855704481852/KxeBgUQAgaMWRmXOAUn1Mb9dtHE5jhwD-lLZpZYs3amrL5Z4KyjQodXby4UCgtgViYQk"

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
    sample_assets = ["https://discord-test.santos.com"]
    send_alert(sample_assets)
