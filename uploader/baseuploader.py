import os
import zipfile
from datetime import datetime

class BaseUploader:
    def __init__(self, retention_count):
        self.retention_count = retention_count

    def zip_file(self, dump_file, db_name, base_backup_dir="zip-db"):
        print("Start zipping dumped database file")
        db_dir = os.path.join(base_backup_dir, db_name)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        zip_file = os.path.join(db_dir, f"{db_name}_{timestamp}.zip")
        try:
            with zipfile.ZipFile(zip_file, 'w') as zf:
                zf.write(dump_file, os.path.basename(dump_file))
            print(f"Database dump compressed: {zip_file}")
            return zip_file
        except Exception as e:
            raise Exception(f"Error compressing file: {e}")
            return None

    def cleanup_local(self, db_name, base_backup_dir="zip-db"):
        print("Clean up data on local")
        try:
            db_dir = os.path.join(base_backup_dir, db_name)
            files = sorted([f for f in os.listdir(db_dir) if f.endswith('.zip')], key=lambda x: os.path.getctime(os.path.join(db_dir, x)), reverse=True)
            for f in files[self.retention_count:]:
                os.remove(os.path.join(db_dir, f))
                print(f"Deleted old local backup: {f}")
        except Exception as e:
            raise Exception(f"Error cleaning up local files: {e}")
