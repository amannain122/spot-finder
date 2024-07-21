import boto3
from botocore.exceptions import ClientError

# AWS region
AWS_S3_REGION_NAME = 'us-east-1'

# Initialize the Athena client with the correct region
athena_client = boto3.client('athena', region_name=AWS_S3_REGION_NAME)

# Replace with your actual query execution ID
query_execution_id = '8edc51a3-e5fe-4ff0-a886-0f62a81db07b'

try:
    # Get the query execution details
    response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
    query_status = response['QueryExecution']['Status']['State']
    print(f"Query Execution Status: {query_status}")
except ClientError as e:
    if e.response['Error']['Code'] == 'InvalidRequestException':
        print("QueryExecution ID not found or invalid.")
    else:
        print(f"An error occurred: {e}")
