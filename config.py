import os
import argparse
from dotenv import load_dotenv

class Config:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Database Backup Script")
        parser.add_argument("--env", type=str, default=".env", help="Path to the .env file")
        args = parser.parse_args()

        print("Loading environment variables")
        load_dotenv(override=True, dotenv_path=args.env)
        
        self.db_config = {
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'port' : os.getenv('DB_PORT')
        }
        self.google = {
            'credential_path' : os.getenv('GOOGLE_CREDENTIALS_PATH'),
            'drive_folder_id': os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        }
        self.drive_type = os.getenv('DRIVE_TYPE')
        self.local_directory = os.getenv('LOCAL_DIRECTORY')
        self.s3_config = {
            'access_key': os.getenv('S3_ACCESS_KEY'),
            'secret_key': os.getenv('S3_SECRET_KEY'),
            'bucket_name': os.getenv('S3_BUCKET_NAME'),
            'region': os.getenv('S3_REGION'),
            'endpoint_url': os.getenv('S3_ENDPOINT_URL'),
            'directory' : os.getenv('S3_DIRECTORY')
        }
        self.backup_retention_count = int(os.getenv('BACKUP_RETENTION_COUNT', 5))

        print("Environment variables are loaded")
