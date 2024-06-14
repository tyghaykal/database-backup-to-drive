import os
import time
from .baseuploader import BaseUploader
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

class GoogleDriveUploader(BaseUploader):
    def __init__(self, config):
        super().__init__(config.backup_retention_count)
        self.credentials_path = config.google['credential_path']
        self.folder_id = config.google['drive_folder_id']
        self.service = self.authenticate()

    def authenticate(self):
        print("Authenticating to Google Drive")
        try:
            credentials = Credentials.from_service_account_file(self.credentials_path)
            auth = build('drive', 'v3', credentials=credentials)
            print("Authenticated to Google Drive")
            return auth
        except Exception as e:
            raise Exception(f"Error authenticating Google Drive: {e}")
            return None

    def upload_to_drive(self, file_path):
        print("Uploading to Google Drive")
        try:
            file_metadata = {
                'name': os.path.basename(file_path),
                'parents': [self.folder_id]
            }
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"File uploaded to Google Drive: {file.get('id')}")

            # Delay to ensure the new file is listed in subsequent queries
            time.sleep(2)
            self.cleanup_drive(file.get('id'))
        except Exception as e:
            raise Exception(f"Error uploading to Google Drive: {e}")

    def cleanup_drive(self, new_file_id):
        print("Clean up data on Google Drive")
        try:
            query = f"'{self.folder_id}' in parents"
            results = self.service.files().list(q=query, fields="files(id, name, createdTime)", orderBy="createdTime desc").execute()
            files = results.get('files', [])

            # Include the new file ID if it's not in the list
            if new_file_id not in [file['id'] for file in files]:
                new_file = self.service.files().get(fileId=new_file_id, fields="id, name, createdTime").execute()
                files.append(new_file)
                files.sort(key=lambda x: x['createdTime'], reverse=True)

            if len(files) > self.retention_count:
                for file in files[self.retention_count:]:
                    self.service.files().delete(fileId=file['id']).execute()
                    print(f"Deleted old backup from Google Drive: {file['name']}")
        except Exception as e:
            raise Exception(f"Error cleaning up Google Drive: {e}")