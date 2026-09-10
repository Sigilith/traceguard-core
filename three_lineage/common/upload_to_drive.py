from __future__ import print_function
import os
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'three lineage bridge.json', SCOPES
        )

        auth_url, _ = flow.authorization_url(prompt='consent')

        print("\nAUTHENTICATION REQUIRED\n")
        print("Opening your browser automatically...\n")

        try:
            subprocess.run(["termux-open", auth_url])
        except Exception:
            print("If the browser didn't open, copy this URL manually:\n")
            print(auth_url)

        print("\nAfter authorizing, paste the code below.\n")
        code = input("Authorization code: ").strip()

        flow.fetch_token(code=code)
        creds = flow.credentials

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_folder(service, name):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

def upload_file(service, folder_id, path):
    file_metadata = {
        'name': os.path.basename(path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def walk_and_upload(service, folder_id, root_path):
    for root, dirs, files in os.walk(root_path):
        for f in files:
            full_path = os.path.join(root, f)
            upload_file(service, folder_id, full_path)

def main():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    folder_id = create_folder(service, "ThreeLineage")
    walk_and_upload(service, folder_id, ".lineage")

    print("\nUPLOAD COMPLETE — All ThreeLineage files are now in Google Drive.\n")

if __name__ == '__main__':
    main()
