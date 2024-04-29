from google_drive_api import get_credentials, download_office_hours_doc

def main():
    """Main function that orchestrates the download of the 'office_hours' document."""
    creds = get_credentials()
    content = download_office_hours_doc(creds)
    if content:
        print("Content of 'office_hours':")
        print(content)

if __name__ == "__main__":
    main()
