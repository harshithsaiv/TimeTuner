import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload  # This line imports MediaIoBaseDownload


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API including exporting a Google Docs file."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Search for the office_hours file
        results = (
            service.files()
            .list(q="name = 'office_hours'", fields="files(id, name, mimeType)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No file named 'office_hours' found.")
            return

        # Assuming the first result is the file we want
        file_id = items[0]['id']
        file_name = items[0]['name']
        file_type = items[0]['mimeType']
        print(f"Found {file_name} ({file_id}) with type {file_type}")

        # Check if the file is a Google Docs document
        if 'application/vnd.google-apps.document' in file_type:
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            content = fh.read().decode('utf-8')
            print("Content of 'office_hours':")
            print(content)
        else:
            print("The file is not a Google Docs document and can't be handled with this script.")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
