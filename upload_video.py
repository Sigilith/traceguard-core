import os
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_PATH = "/storage/emulated/0/DCIM/Screen recordings/Screen_Recording_20260910_100434_Termux.mp4"
REDIRECT_URI = "http://localhost"

def upload_video():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            flow.redirect_uri = REDIRECT_URI
            
            auth_url, _ = flow.authorization_url(prompt="consent")
            print(f"\n[?] Open this link on your phone/browser to authorize:\n\n{auth_url}\n")
            
            raw_input_val = input("Paste the authorization code or full redirect URL here: ").strip()
            
            if "code=" in raw_input_val:
                if not raw_input_val.startswith("http"):
                    raw_input_val = "http://localhost/?" + raw_input_val
                parsed_url = urlparse(raw_input_val)
                code = parse_qs(parsed_url.query).get("code", [raw_input_val])[0]
            else:
                code = raw_input_val

            flow.fetch_token(code=code)
            creds = flow.credentials
            
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": "Why Cloud AI Safety is Broken (Building a Local Governance Vault)",
            "description": "Most AI safety guardrails rely on cloud APIs and fragile software wrappers. Three-Lineage is a self-sovereign runtime governance engine running locally via Termux and local hardware.\n\nWatch live as the engine intercepts high-risk adversarial telemetry spikes ([3.4, 4.1, 2.8]), triggers the Derek Gate triple-lock containment, seals an immutable JSONL audit block, and cleanly restores baseline stability.\n\n#AISafety #RuntimeGovernance #SystemsEngineering #CryptographicSecurity #Termux #LocalAI #IndependentResearch",
            "tags": ["AI safety", "runtime governance", "cryptographic security", "independent research", "local AI", "Termux", "AI containment", "autonomous systems", "cybersecurity engineering"],
            "categoryId": "28"  
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(VIDEO_PATH, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print("\n[+] Uploading video to YouTube...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"[+] Upload progress: {int(status.progress() * 100)}%")

    print(f"\n[+] Upload complete! Video ID: {response.get('id')}")

if __name__ == "__main__":
    upload_video()
