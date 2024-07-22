import os
import pandas as pd

# Load the CSV file
file_path = '/home/ubuntu/spot-finder/notebooks/Yolo-V8/SampleAthena/parking_status/parking_status.csv'
parking_data = pd.read_csv(file_path)

# Function to calculate fare based on duration
def calculate_fare(duration_hours):
    if duration_hours <= 1:
        return 2.50  # Base fare for up to 1 hour
    elif duration_hours <= 6:
        return 2.50 + (duration_hours - 1) * 1.50  # Additional fare for 2-6 hours
    else:
        return 10 + (duration_hours - 6) * 1  # Additional fare for more than 6 hours

# Initialize a list to store results
results = []

# Process each parking spot
for spot in ['SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7']:
    in_time = None
    customer_id = 101  # Starting CustomerID from 101

    for index, row in parking_data.iterrows():
        if row[spot] == 'occupied' and in_time is None:
            in_time = pd.to_datetime(row['Timestamp'])
        elif row[spot] == 'empty' and in_time is not None:
            out_time = pd.to_datetime(row['Timestamp'])
            duration = (out_time - in_time).total_seconds() / 3600  # Duration in hours
            fare = calculate_fare(duration)
            results.append([spot, customer_id, in_time, out_time, duration, f"${fare:.2f}"])
            in_time = None
            customer_id += 1  # Increment CustomerID for the next customer

            # Update the parking status to 'available'
            parking_data.at[index, spot] = 'available'

# Convert results to a DataFrame
results_df = pd.DataFrame(results, columns=['ParkingSpotID', 'CustomerID', 'InTime', 'OutTime', 'DurationHours', 'Fare'])

# Ensure the output directory exists
output_directory = '/home/ubuntu/spot-finder/pipeline/model-related/data'
os.makedirs(output_directory, exist_ok=True)

# Save the results to a new CSV file
output_file_path = os.path.join(output_directory, 'parking_fares.csv')
results_df.to_csv(output_file_path, index=False)

# Save the updated original CSV file
updated_file_path = '/home/ubuntu/spot-finder/pipeline/model-related/data/parking_status.csv'
parking_data.to_csv(updated_file_path, index=False)

print(results_df.head())
print(parking_data.head())
