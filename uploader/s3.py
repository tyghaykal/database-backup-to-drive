from .baseuploader import BaseUploader
import boto3
import os
from botocore.exceptions import NoCredentialsError

class S3Uploader(BaseUploader):
    def __init__(self, s3_config, retention_count):
        super().__init__(retention_count)
        self.s3_config = s3_config
        self.s3 = self.authenticate()

    def authenticate(self):
        print("Authenticating to S3")
        try:
            auth = boto3.client('s3',
                                aws_access_key_id=self.s3_config['access_key'],
                                aws_secret_access_key=self.s3_config['secret_key'],
                                region_name=self.s3_config['region'],
                                endpoint_url=self.s3_config['endpoint_url'])
            print("Authenticated to S3")
            return auth
        except NoCredentialsError as e:
            raise Exception(f"Error authenticating S3: {e}")
            return None

    def upload_to_s3(self, file_path):
        print("Uploading to S3")
        try:
            file_name = os.path.basename(file_path)
            s3_key = os.path.join(self.s3_config['directory'], file_name) if self.s3_config['directory'] else file_name
            self.s3.upload_file(file_path, self.s3_config['bucket_name'], s3_key)
            print(f"File uploaded to S3: {os.path.basename(file_path)}")
            self.cleanup_s3()
        except Exception as e:
            raise Exception(f"Error uploading to S3: {e}")

    def cleanup_s3(self):
        print("Clean up data on S3")
        try:
            objects = self.s3.list_objects_v2(Bucket=self.s3_config['bucket_name'], Prefix=self.s3_config['directory'])
            if 'Contents' in objects:
                files = sorted(objects['Contents'], key=lambda x: x['LastModified'], reverse=True)
                if len(files) > self.retention_count:
                    for file in files[self.retention_count:]:
                        self.s3.delete_object(Bucket=self.s3_config['bucket_name'], Key=file['Key'])
                        print(f"Deleted old backup from S3: {file['Key']}")
        except (NoCredentialsError, ClientError) as e:
            raise Exception(f"Error cleaning up S3: {e}")
