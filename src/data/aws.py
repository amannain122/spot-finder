import boto3
from botocore.exceptions import NoCredentialsError

# AWS credentials (replace these with your own)
AWS_ACCESS_KEY = 'AKIA5FTZDJFWTITGXH5B'
AWS_SECRET_KEY = 'esBkizsCWrMfA/OnmQdLGcp+/Oy3Ui2RuDwmVZxZ'
AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'spotfinder-data-bucket'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

