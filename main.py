from google_drive_api import get_credentials, download_office_hours_doc
from chatgpt_interface import chat_with_chatgpt

def main():
    """Main function that orchestrates the document download and interaction with ChatGPT."""
    creds = get_credentials()
    document_content = download_office_hours_doc(creds)
    if document_content:
        print("Successfully downloaded 'office_hours' document content.")
        print(document_content)
        chat_with_chatgpt(document_content)

if __name__ == "__main__":
    main()
