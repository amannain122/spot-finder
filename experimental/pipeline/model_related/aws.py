import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

import data_loader as dlu

spot_finder_dir = dlu.find_spot_finder_dir()
# Load environment variables from .env file
load_dotenv(os.path.join(spot_finder_dir, '.env'))

# Constants for AWS region and S3 bucket name
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = 'us-east-1'
s3_bucket_name = 'spotfinder-data-bucket'
s3_folder = 'SampleAthena/'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

def upload_to_s3(file_path):
    """
    Upload a file to AWS S3 bucket.
    """
    file_name = os.path.basename(file_path)
    s3_key = os.path.join(s3_folder, file_name)
    try:
        s3.upload_file(file_path, s3_bucket_name, s3_key)
        print(f"{file_name} uploaded successfully to S3 bucket.")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


