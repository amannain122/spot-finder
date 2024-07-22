import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

csv_path = 'SampleAthena/parking_status/parking_status.csv'
s3_bucket_name = 'spotfinder-data-bucket'
role_arn = 'arn:aws:s3:::spotfinder-data-bucket/SampleAthena/parking_status/'

try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name='us-east-1'
    )

    s3_client.upload_file(csv_path, s3_bucket_name, csv_path)
    print('reachedHere7')
    print(f"File uploaded to S3 bucket {s3_bucket_name} successfully.")
except NoCredentialsError:
    print("Credentials not available for uploading to S3.")
except Exception as e:
    print(f"Error uploading to S3: {e}")