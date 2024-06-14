import subprocess
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error

class DatabaseDumper:
    def __init__(self, config):
        self.config_db = config.db_config
        self.config_local_directory = config.local_directory
        self.config_compression_level = config.compression_level
        self.retention_count = config.backup_retention_count


    def create_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.config_db['host'],
                user=self.config_db['user'],
                passwd=self.config_db['password'],
                port=self.config_db['port']
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            raise Exception(f"The error '{e}' occurred")
        return connection

    def get_database_character_set(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT default_character_set_name FROM information_schema.SCHEMATA WHERE schema_name = '{self.config_db['database']}';")
            result = cursor.fetchone()
            if result:
                charset = result[0]
                if charset != '':
                    return charset
                else :
                    return "utf8"
                
            else:
                raise Exception(f"No character set found for database '{self.config_db['database']}'")    
        except Error as e:
            raise Exception(f"The error '{e}' occurred")
        

    def dump_database(self):
        print("Starting dump database")

        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if not os.path.exists('dump-db'):
            os.makedirs('dump-db')
        compressed_dir = os.path.join(self.config_local_directory, self.config_db['database'])
        if not os.path.exists(compressed_dir):
            os.makedirs(compressed_dir)
        dump_file = f"{self.config_db['database']}_{timestamp}.sql.gz"
        full_location = os.path.join(compressed_dir, f"{dump_file}")
        try:
            connection = self.create_connection()
            charset = self.get_database_character_set(connection)

            dump_command = (
                f"mysqldump --column-statistics=0 -R -E --default-character-set={charset} "
                f"--force --opt "
                f"-u {self.config_db['user']} "
                f"-p{self.config_db['password']} "
                f"-h {self.config_db['host']} "
                f"--port {self.config_db['port']} "
                f"{self.config_db['database']} | gzip -{self.config_compression_level} > {full_location}"
            )
            subprocess.run(dump_command, shell=True, check=True)
            print(f"Database dump successful: {full_location}")
            return full_location
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error dumping database: {e}")
        
    def cleanup_local(self):
        print("Clean up data on local")
        try:
            db_dir = os.path.join(self.config_local_directory, self.config_db['database'])
            files = sorted([f for f in os.listdir(db_dir) if f.endswith('.gz')], key=lambda x: os.path.getctime(os.path.join(db_dir, x)), reverse=True)
            for f in files[self.retention_count:]:
                os.remove(os.path.join(db_dir, f))
                print(f"Deleted old local backup: {f}")
        except Exception as e:
            raise Exception(f"Error cleaning up local files: {e}")
