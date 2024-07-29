import time
import boto3
import environ
import pandas as pd
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.exceptions import ClientError

env = environ.Env()

AWS_S3_REGION_NAME = 'us-east-1'
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""

METADATA = [
    {
        "ParkingLotID": "PL01",
        "URL": "https://www.youtube.com/watch?v=HBDD3j5so0g",
        "Location": "49.00426480950375, -122.73464953172447",
        "Number of Spots": 13,
        "ROI": "PL01.csv",
        "Address": "120 176 St, Surrey, BC V3S 9S2"
    },
    {
        "ParkingLotID": "PL02",
        "URL": "https://www.youtube.com/watch?v=EPKWu223XEg",
        "Location": "",
        "Number of Spots": 23,
        "ROI": "PL02.csv",
        "Address": ""
    },
    {
        "ParkingLotID": "PL03",
        "URL": "https://www.youtube.com/watch?v=kC6_JqEt3GA",
        "Location": "51.08961722612397, -115.35780639113904",
        "Number of Spots": 5,
        "ROI": "PL03.csv",
        "Address": "630 8 St, Canmore, AB T1W 2B5"
    }
]

athena_client = boto3.client(
    service_name='athena',
    region_name='us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


query = "SELECT * FROM athena_spot_finder.parking_lots;"
database = "sample_db"
output_location = "s3://spotfinder-data-bucket/Athena_output/"


def query_athena(query, database, output_location):
    try:
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': database},
            ResultConfiguration={'OutputLocation': output_location},
        )
        query_execution_id = response['QueryExecutionId']
        return query_execution_id
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("AWS credentials not found or incomplete: ", str(e))
    except ClientError as e:
        print("Client error: ", str(e))
    except Exception as e:
        print("An error occurred: ", str(e))


def get_query_results(query_execution_id):

    # Poll for query completion
    while True:
        response = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        print(f"Current status: {status}. Waiting for query to complete...")
        time.sleep(5)  # Wait for 5 seconds before checking again

    if status == 'SUCCEEDED':
        print("Query succeeded. Fetching results...")
        result = athena_client.get_query_results(
            QueryExecutionId=query_execution_id)
        return result
    else:
        raise Exception(
            f"Query failed or was cancelled. Final status: {status}")


def results_to_dataframe(results):
    rows = results['ResultSet']['Rows']
    columns = [col['VarCharValue'] for col in rows[0]['Data']]
    data = [[col['VarCharValue'] for col in row['Data']] for row in rows[1:]]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('out.csv', index=False)

    file_path = 'out.csv'
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting header and data rows
    data_rows = [line.strip().split(',') for line in lines[1:]]

    # Manually fixing the header and data rows
    fixed_header = ['ParkingLotID', 'Timestamp', 'SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7',
                    'SP8', 'SP9', 'SP10', 'SP11', 'SP12', 'SP13', 'SP14', 'SP15', 'SP16', 'SP17',
                    'SP18', 'SP19', 'SP20', 'SP21', 'SP22', 'SP23']

    # Filtering the data rows to ensure correct length and structure
    corrected_data_rows = [
        row for row in data_rows if len(row) == len(fixed_header)]

    # Creating the DataFrame with corrected header and data rows
    corrected_data = pd.DataFrame(corrected_data_rows, columns=fixed_header)

    # Stripping extraneous quotes and spaces from the data entries
    corrected_data = corrected_data.map(lambda x: x.strip().strip('"'))

    # Removing the first row which contains the column headers instead of actual data
    corrected_data = corrected_data.iloc[1:].reset_index(drop=True)

    # Converting the cleaned DataFrame to an array of objects (list of dictionaries)
    array_of_objects = corrected_data.to_dict(orient='records')

    return array_of_objects
