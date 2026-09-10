import time
import requests

PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"  # Change to api-m.paypal.com for live

def get_paypal_access_token(client_id: str, client_secret: str):
    url = f"{PAYPAL_API_BASE}/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    return response.json().get("access_token")

def create_paypal_invoice(access_token: str, recipient_email: str, amount: float, item_name: str):
    url = f"{PAYPAL_API_BASE}/v1/invoicing/invoices"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    invoice_payload = {
        "detail": {
            "invoice_number": f"DEREK-{int(time.time())}",
            "currency_code": "GBP",
            "note": "Automated Sentinel Mesh telemetry processing fee."
        },
        "invoicer": {
            "email_address": "Kynash1@outlook.com"
        },
        "primary_recipients": [{
            "billing_info": {
                "email_address": recipient_email
            }
        }],
        "items": [{
            "name": item_name,
            "quantity": "1",
            "unit_amount": {
                "currency": "GBP",
                "value": f"{amount:.2f}"
            }
        }]
    }
    
    response = requests.post(url, headers=headers, json=invoice_payload)
    if response.status_code == 201:
        invoice_data = response.json()
        print(f"[+] PayPal Invoice Created: {invoice_data.get('href')}")
        return invoice_data
    else:
        print(f"[-] Failed to create PayPal invoice: {response.text}")
        return None

if __name__ == "__main__":
    print("[*] PayPal module loaded successfully.")
