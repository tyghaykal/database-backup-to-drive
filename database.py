import subprocess
import os

class DatabaseDumper:
    def __init__(self, db_config):
        self.db_config = db_config

    def dump_database(self):
        print("Starting dump database")
        if not os.path.exists('dump-db'):
            os.makedirs('dump-db')
        dump_file = f"dump-db/db_dump_{self.db_config['database']}.sql"
        try:
            dump_command = (
                f"mysqldump --column-statistics=0 -u {self.db_config['user']} "
                f"-p{self.db_config['password']} "
                f"-h {self.db_config['host']} "
                f"--port {self.db_config['port']} "
                f"{self.db_config['database']} > {dump_file}"
            )
            subprocess.run(dump_command, shell=True, check=True)
            print(f"Database dump successful: {dump_file}")
            return dump_file
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error dumping database: {e}")
            return None
