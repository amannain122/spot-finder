import boto3

# Initialize the Athena client
athena_client = boto3.client('athena', region_name='us-east-1')

def list_query_executions():
    response = athena_client.list_query_executions()
    query_execution_ids = response['QueryExecutionIds']
    return query_execution_ids

if __name__ == "__main__":
    executions = list_query_executions()
    for execution in executions:
        print(execution)
