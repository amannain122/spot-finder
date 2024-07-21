import boto3
import time
import pandas as pd
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.conf import settings

def execute_athena_query(query, database, output_location):
    client = boto3.client('athena', region_name=settings.AWS_S3_REGION_NAME)

    try:
        response = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': database
            },
            ResultConfiguration={
                'OutputLocation': output_location
            }
        )
        return response['QueryExecutionId']
    except NoCredentialsError:
        raise Exception("AWS credentials not found.")
    except PartialCredentialsError:
        raise Exception("Incomplete AWS credentials provided.")
    except client.exceptions.InvalidRequestException as e:
        raise Exception(f"InvalidRequestException: {str(e)}")

def get_query_results(query_execution_id):
    client = boto3.client('athena')
    max_retries = 10
    state = 'RUNNING'
    while max_retries > 0 and state in ['RUNNING', 'QUEUED']:
        response = client.get_query_execution(QueryExecutionId=query_execution_id)
        state = response['QueryExecution']['Status']['State']
        if state == 'SUCCEEDED':
            break
        elif state == 'FAILED':
            raise Exception(f"Query failed: {response['QueryExecution']['Status']['StateChangeReason']}")
        elif state == 'CANCELLED':
            raise Exception("Query was cancelled")
        time.sleep(5)
        max_retries -= 1

    if state != 'SUCCEEDED':
        raise Exception(f"Query did not succeed within the maximum retry limit: {state}")

    result = client.get_query_results(QueryExecutionId=query_execution_id)
    columns = [col['Label'] for col in result['ResultSet']['ResultSetMetadata']['ColumnInfo']]
    rows = [row['Data'] for row in result['ResultSet']['Rows'][1:]]
    data = [{col: (datum['VarCharValue'] if 'VarCharValue' in datum else None) for col, datum in zip(columns, row)} for row in rows]

    df = pd.DataFrame(data, columns=columns)
    return df

# Usage example
if __name__ == "__main__":
    query = "SELECT * FROM sample_db.sampletable LIMIT 10;"
    database = "sample_db"
    output_location = "s3://spotfinder-data-bucket/Athena-output/"
    
    try:
        query_execution_id = execute_athena_query(query, database, output_location)
        print(f"Query Execution ID: {query_execution_id}")
        
        # Simulate waiting for the query to complete
        time.sleep(10)
        
        results_df = get_query_results(query_execution_id)
        print(results_df)
    except Exception as e:
        print(f"Error: {e}")
