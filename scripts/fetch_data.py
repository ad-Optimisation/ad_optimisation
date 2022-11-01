import boto3
import defaults as defs


def fetch_data(_bucket_name: str = defs.bucket_name,
               _from_path: str = defs.from_path, _to_path: str = defs.to_path):
    s3 = boto3.client('s3')
    s3.download_file(_bucket_name, _from_path, _to_path)
