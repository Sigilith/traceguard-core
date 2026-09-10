import os, sys
from urllib.parse import urlparse, parse_qs
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
flow.redirect_uri = "http://localhost"
auth_url, _ = flow.authorization_url(prompt='consent')

print("\n" + "="*60)
print("1. OPEN THIS LINK IN YOUR BROWSER:")
print(auth_url)
print("="*60 + "\n")

code_input = input("2. PASTE THE FULL REDIRECT URL HERE (http://localhost/?state=...):\n> ").strip()

if "code=" in code_input:
    parsed = urlparse(code_input)
    code = parse_qs(parsed.query).get("code")[0]
else:
    code = code_input

try:
    flow.fetch_token(code=code)
except Exception as e:
    print(f"\n[!] Token failed (likely expired). Error: {e}")
    sys.exit(1)

print("\nUploading next technical walkthrough... please wait.")
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=flow.credentials)
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "categoryId": "28",
            "title": "Building Axiomos: Autonomous Policy Engine Enforcement in Python",
            "description": "A deep-dive technical demonstration of Axiomos and TraceGuard Core, focusing on symbolic system verification, automated policy enforcement, and secure Python backend architecture.",
            "tags": ["PythonProgramming", "PolicyEngine", "SoftwareArchitecture", "CyberSecurity", "AutomatedGovernance", "DevOps", "SystemsEngineering"]
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=googleapiclient.http.MediaFileUpload("terminal_output.mp4", chunksize=-1, resumable=True)
)
response = request.execute()
print(f"\n[+] High-value video uploaded successfully! Video ID: {response.get('id')}")
