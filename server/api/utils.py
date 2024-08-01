import time
import boto3
import environ
import pandas as pd
import asyncio
from aiobotocore.session import get_session
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

env = environ.Env()

AWS_S3_REGION_NAME = 'us-east-1'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

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


async def query_athena(query, database, output_location):
    session = get_session()
    async with session.create_client('athena', region_name=AWS_S3_REGION_NAME,
                                     aws_access_key_id=AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY) as client:
        try:
            response = await client.start_query_execution(
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


async def get_query_results(query_execution_id):
    session = get_session()
    async with session.create_client('athena', region_name=AWS_S3_REGION_NAME,
                                     aws_access_key_id=AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY) as client:

        while True:
            response = await client.get_query_execution(
                QueryExecutionId=query_execution_id)
            status = response['QueryExecution']['Status']['State']
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            # print(f"Current status: {
            #       status}. Waiting for query to complete...")
            await asyncio.sleep(5)  # Wait for 5 seconds before checking again

        if status == 'SUCCEEDED':
            print("Query succeeded. Fetching results...")
            result = await client.get_query_results(
                QueryExecutionId=query_execution_id)
            return result
        else:
            raise Exception(
                f"Query failed or was cancelled. Final status: {status}")


def results_to_dataframe(athena_response):
    # Step 1: Extract column names
    columns = [col['VarCharValue']
               for col in athena_response['ResultSet']['Rows'][0]['Data']]

    # Step 2: Extract data rows
    rows = [
        [data['VarCharValue'] if 'VarCharValue' in data else None for data in row['Data']]
        for row in athena_response['ResultSet']['Rows'][1:]
    ]

    # Step 3: Convert to DataFrame
    df = pd.DataFrame(rows, columns=columns)

    df.columns = df.iloc[0]  # Set the first row as header
    df = df[1:]  # Remove the first row from the data

    array_of_objects = df.to_dict(orient='records')

    return array_of_objects


def merge_data(metadata, athena_data):

    data = athena_data

    # Iterate through the metadata and match it with the data
    parking_lots = []
    for idx, lot in enumerate(metadata):
        lot_spots = [row for row in data if row["ParkingLotID"]
                     == lot["ParkingLotID"]]

        if lot_spots:
            # Assuming that spot columns are named SP1, SP2,...SP23
            spots_list = [{"spot": f"SP{i+1}", "status": lot_spots[0].get(f"SP{i+1}", "empty")}
                          for i in range(23)]

            # Parse coordinates if available
            coordinates = {"latitude": 0.0, "longitude": 0.0}
            if lot["Location"]:
                lat, lon = map(float, lot["Location"].split(","))
                coordinates = {"latitude": lat, "longitude": lon}

            # Calculate total, available, and reserved spots
            total_spots = lot["Number of Spots"]
            available_spots = sum(
                1 for spot in spots_list if spot["status"] == "empty")
            reserved_spots = total_spots - available_spots

            # Build the parking lot dictionary
            parking_lots.append({
                "id": idx + 1,
                "parking_id": lot["ParkingLotID"],
                "coordinates": coordinates,
                "total_spots": total_spots,
                "available_spots": available_spots,
                "reserved_spots": reserved_spots,
                "address": lot["Address"],
                "image": lot["URL"],
                "spots": spots_list
            })
    return parking_lots
