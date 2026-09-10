import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
flow.redirect_uri = "http://localhost"
flow.fetch_token(code="4/0ATsMZqDXnYtiQxa0VcMEVIwqGAnE-hwpL_RAduX0y8tSAX8L57Lw-NeH5xtP_fsdMxCI4Q")
credentials = flow.credentials

youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "categoryId": "28",
            "title": "Building an Autonomous Governance Kernel from Scratch",
            "description": "A complete technical walkthrough of Three-Lineage, TraceGuard, and Sigilith.",
            "tags": ["CyberSecurity", "Python", "SystemsEngineering", "AutonomousAgents"]
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=googleapiclient.http.MediaFileUpload("terminal_output.mp4", chunksize=-1, resumable=True)
)
response = request.execute()
print(f"\n[+] Video uploaded successfully! Video ID: {response.get('id')}")
