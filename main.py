import os
from config import Config
from database import DatabaseDumper
from uploader.googledrive import GoogleDriveUploader
from uploader.s3 import S3Uploader
from uploader.local import LocalSaver
from datetime import datetime

def main():
    try:
        config = Config()
        

        db_dumper = DatabaseDumper(config)
        dump_file = db_dumper.dump_database()
        if dump_file:
            if config.drive_type == 'google-drive':
                uploader = GoogleDriveUploader(config)
            elif config.drive_type == 's3':
                uploader = S3Uploader(config.s3_config, config.backup_retention_count)
            elif config.drive_type == 'local':
                uploader = LocalSaver(config.backup_retention_count)
            else:
                print("Invalid disk type specified in .env. Exiting.")
                return
            
            if dump_file:
                if config.drive_type == 'google-drive':
                    uploader.upload_to_drive(dump_file)
                elif config.drive_type == 's3':
                    uploader.upload_to_s3(dump_file)
                    
                db_dumper.cleanup_local()

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == '__main__':
    main()
