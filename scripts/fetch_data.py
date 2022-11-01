import boto3
from defaults import *

s3 = boto3.client('s3')
s3.download_file(bucket_name, path, "data/Challenge_Data.zip")
