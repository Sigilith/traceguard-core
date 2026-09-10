import os
import msal
import requests

CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
TENANT_ID = "common"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

def get_access_token():
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"[-] Auth Error: {result.get('error_description')}")
        return None

def send_outreach_graph(to_email, company_name):
    token = get_access_token()
    if not token:
        return

    endpoint = "https://graph.microsoft.com/v1.0/users/ThreeLineage@outlook.com/sendMail"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    email_payload = {
        "message": {
            "subject": f"Autonomous Runtime Security Framework for {company_name}",
            "body": {
                "contentType": "HTML",
                "content": f"<p>Dear Security Lead at <strong>{company_name}</strong>,<br><br>I developed ThreeLineage as an independent deterministic governance framework—decoupling risk evaluation from agent logic via TraceGuard, AXIOMOS, and Derek.</p>"
            },
            "toRecipients": [
                {"emailAddress": {"address": to_email}}
            ]
        },
        "saveToSentItems": "true"
    }

    response = requests.post(endpoint, headers=headers, json=email_payload)
    if response.status_code == 202:
        print(f"[+] Microsoft Graph: Outreach dispatched successfully to {to_email}")
    else:
        print(f"[-] Graph Send Failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("==================================================")
    print(" THREE-LINEAGE GRAPH API GATEWAY ACTIVE (SOLO)")
    print("==================================================")
