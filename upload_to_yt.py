import os
from urllib.parse import urlparse, parse_qs
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(file_path, title, description, tags):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES)
    flow.redirect_uri = "http://localhost"

    auth_url, _ = flow.authorization_url(prompt='consent')

    print("\n" + "="*50)
    print("OPEN THIS LINK IN YOUR BROWSER:")
    print(auth_url)
    print("="*50 + "\n")

    code_input = input("After authorizing, paste the FULL redirected URL (or just the code) here: ").strip()

    if "code=" in code_input:
        parsed = urlparse(code_input)
        code = parse_qs(parsed.query).get("code")
        code = code[0] if code else code_input
    else:
        code = code_input

    flow.fetch_token(code=code)
    credentials = flow.credentials

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "28",
                "title": title,
                "description": description,
                "tags": tags
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"\n[+] Video uploaded successfully! Video ID: {response.get('id')}")

if __name__ == "__main__":
    upload_video(
        file_path="terminal_output.mp4",
        title="Building an Autonomous Governance Kernel from Scratch",
        description="A complete technical walkthrough of Three-Lineage, TraceGuard, and Sigilith.",
        tags=["CyberSecurity", "Python", "SystemsEngineering", "AutonomousAgents"]
    )
