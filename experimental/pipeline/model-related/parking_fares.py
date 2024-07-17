import pandas as pd

# Load the CSV file
parking_status_path = 'D:\spot-finder\data\parking_status.csv'
parking_data = pd.read_csv(parking_status_path)

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

# Process each row in the data for parking spots SP1 to SP23
for spot in [f'SP{i}' for i in range(1, 24)]:
    in_time = None
    customer_id = 101  # Starting CustomerID from 101

    for index, row in parking_data.iterrows():
        parking_lot_id = row['ParkingLotID']
        if row[spot] == 'occupied' and in_time is None:
            in_time = pd.to_datetime(row['Timestamp'])
        elif row[spot] in ['available', 'empty'] and in_time is not None:
            out_time = pd.to_datetime(row['Timestamp'])
            duration = (out_time - in_time).total_seconds() / 3600  # Duration in hours
            fare = calculate_fare(duration)
            results.append([parking_lot_id, spot, customer_id, in_time, out_time, duration, f"${fare:.2f}"])
            in_time = None
            customer_id += 1  # Increment CustomerID for the next customer

# Convert results to a DataFrame
results_df = pd.DataFrame(results, columns=['ParkingLotID', 'ParkingSpotID', 'CustomerID', 'InTime', 'OutTime', 'DurationHours', 'Fare'])

# Save the results to a new CSV file
results_file_path = 'D:\spot-finder\data\parking_fares_calculated.csv'
results_df.to_csv(results_file_path, index=False)

# Display the first few rows of the results
print(results_df.head())
