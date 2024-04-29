# google_drive_api.py
import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials(token_file='token.json', creds_file='credentials.json'):
    """Retrieve or create credentials based on token and credentials files."""
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds

def download_office_hours_doc(creds):
    """Download content of the 'office_hours' document as plain text."""
    try:
        service = build("drive", "v3", credentials=creds)
        results = service.files().list(q="name = 'office_hours'", fields="files(id, name, mimeType)").execute()
        items = results.get("files", [])

        if not items:
            print("No file named 'office_hours' found.")
            return None

        file_id = items[0]['id']
        request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.seek(0)
        content = fh.read().decode('utf-8')
        return content
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
