import boto3
from botocore.exceptions import ClientError
from io import BytesIO
from typing import List
from data_pipeline.config import data_settings

class S3Storage:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url = f"http://{data_settings.MINIO_ENDPOINT}",
            aws_access_key_id = data_settings.MINIO_ACCESS_KEY,
            aws_secret_access_key = data_settings.MINIO_SECRET_KEY,
            region_name="us-east-1",
        )

        self.bucket = data_settings.MINIO_BUCKET
    

    def ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket)
            print(f"Bucket is already exist: '{self.bucket}'")
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket)
            print(f"Bucket created: '{self.bucket}'")

    def upload_bytes(self, data: bytes, object_key: str) -> str:
        self.client.put_object(Bucket=self.bucket, Key=object_key, Body=data)
        print(f"Uploaded bytes → s3://{self.bucket}/{object_key}")
        return f"s3://{self.bucket}/{object_key}"

    def upload_file(self, local_file_path: str, object_key: str) -> str:
        self.client.upload_file(local_file_path, self.bucket, object_key)
        print(f"Uploaded file → s3://{self.bucket}/{object_key}")
        return f"s3://{self.bucket}/{object_key}"

    def download_to_buffer(self, object_key: str) -> BytesIO:
        buffer = BytesIO()
        self.client.download_fileobj(self.bucket, object_key, buffer)
        buffer.seek(0)
        print(f"Downloaded s3://{self.bucket}/{object_key} to buffer")
        return buffer

    def list_obj(self, prefix: str) -> List[str]:
        response = self.client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            return []