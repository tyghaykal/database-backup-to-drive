import os
import gzip
from datetime import datetime

class BaseUploader:
    def __init__(self, retention_count):
        self.retention_count = retention_count

    def zip_file(self, dump_file, db_name, base_backup_dir="zip-db", compression_level=6):
        print("Start zipping dumped database file")
        if dump_file is None or not os.path.exists(dump_file):
            raise ValueError("The dump file does not exist or is not specified.")
        
        db_dir = os.path.join(base_backup_dir, db_name)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        compressed_file = os.path.join(db_dir, f"{db_name}_{timestamp}.gz")
        try:
            with open(dump_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb', compresslevel=compression_level) as f_out:
                    f_out.writelines(f_in)
            print(f"Database dump compressed: {compressed_file}")
            return compressed_file
        except Exception as e:
            raise Exception(f"Error compressing file: {e}")
            return None

    def cleanup_local(self, db_name, base_backup_dir="zip-db"):
        print("Clean up data on local")
        try:
            db_dir = os.path.join(base_backup_dir, db_name)
            files = sorted([f for f in os.listdir(db_dir) if f.endswith('.gz')], key=lambda x: os.path.getctime(os.path.join(db_dir, x)), reverse=True)
            for f in files[self.retention_count:]:
                os.remove(os.path.join(db_dir, f))
                print(f"Deleted old local backup: {f}")
        except Exception as e:
            raise Exception(f"Error cleaning up local files: {e}")
