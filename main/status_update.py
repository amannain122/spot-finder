import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
root_dir = Path(__file__).resolve().parents[1]
dotenv_path = root_dir / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Define absolute file path and S3 details
# csv_path = str((root_dir / 'src' / 'data' / 'parking_status.csv').resolve())
csv_path = os.path.join(root_dir, 'src/data/parking_status.csv')
s3_bucket_name = 'spotfinder-data-bucket'
s3_folder = 'SampleAthena/'
role_arn = 'arn:aws:s3:::spotfinder-data-bucket/SampleAthena/parking_status/'

try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        region_name='us-east-1'
    )

    # Check if the CSV path exists
    # Ensure os.path.exists() is called correctly
    file_exists = os.path.exists(csv_path)
    if not file_exists:
        raise FileNotFoundError(f"The file {csv_path} does not exist")
    
    file_name = os.path.basename(csv_path)
    s3_key = os.path.join(s3_folder, file_name)

    s3_client.upload_file(csv_path, s3_bucket_name, s3_key)
    print('reachedHere7')
    print(f"File uploaded to S3 bucket {s3_bucket_name, s3_folder} successfully.")
except NoCredentialsError:
    print("Credentials not available for uploading to S3.")
except Exception as e:
    print(f"Error uploading to S3: {e}")
