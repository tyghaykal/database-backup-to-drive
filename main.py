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
        

        db_dumper = DatabaseDumper(config.db_config)
        dump_file = db_dumper.dump_database()
        if dump_file:
            if config.drive_type == 'google-drive':
                uploader = GoogleDriveUploader(config.google['credential_path'], config.google['drive_folder_id'],config.backup_retention_count)
            elif config.drive_type == 's3':
                uploader = S3Uploader(config.s3_config, config.backup_retention_count)
            elif config.drive_type == 'local':
                uploader = LocalSaver(config.backup_retention_count)
            else:
                print("Invalid disk type specified in .env. Exiting.")
                return

            zip_file_path = uploader.zip_file(dump_file, config.db_config['database'], config.local_directory, config.compression_level)
            
            if zip_file_path:
                if config.drive_type == 'google-drive':
                    uploader.upload_to_drive(zip_file_path)
                elif config.drive_type == 's3':
                    uploader.upload_to_s3(zip_file_path)
                    
                uploader.cleanup_local(config.db_config['database'], config.local_directory)

            # Clean up dump file if it wasn't already deleted during zipping
            if os.path.exists(dump_file):
                os.remove(dump_file)

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == '__main__':
    main()
