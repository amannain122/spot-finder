import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load the occupancy data from CSV
csv_file = "/Users/tinaukanwune/Desktop/spotfinder/occupancy_data.csv"
data = pd.read_csv(csv_file)

# Convert timestamp to datetime object with specific format
data['timestamp'] = pd.to_datetime(data['timestamp'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Drop rows with NaT (Not a Time) values that couldn't be parsed
data.dropna(subset=['timestamp'], inplace=True)

# Set timestamp as index
data.set_index('timestamp', inplace=True)

# Resample data to get hourly average occupancy
hourly_data = data.resample('h').mean()

# Plot occupancy percentage over time
plt.figure(figsize=(14, 7))
plt.plot(hourly_data.index, hourly_data['occupancy_percentage'], marker='o', linestyle='-')
plt.title('Hourly Average Occupancy Percentage')
plt.xlabel('Time')
plt.ylabel('Occupancy Percentage (%)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("/Users/tinaukanwune/Desktop/spotfinder/hourly_occupancy_plot.png")
plt.show()

# Calculate daily summary statistics
daily_summary = data.resample('D').agg({
    'occupancy_percentage': ['mean', 'max', 'min']
})

# Plot daily occupancy statistics
plt.figure(figsize=(14, 7))
plt.plot(daily_summary.index, daily_summary['occupancy_percentage']['mean'], marker='o', linestyle='-', label='Daily Mean')
plt.plot(daily_summary.index, daily_summary['occupancy_percentage']['max'], marker='o', linestyle='-', label='Daily Max')
plt.plot(daily_summary.index, daily_summary['occupancy_percentage']['min'], marker='o', linestyle='-', label='Daily Min')
plt.title('Daily Occupancy Statistics')
plt.xlabel('Date')
plt.ylabel('Occupancy Percentage (%)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/Users/tinaukanwune/Desktop/spotfinder/daily_occupancy_stats.png")
plt.show()

# Insights generation
average_occupancy = hourly_data['occupancy_percentage'].mean()
peak_occupancy = hourly_data['occupancy_percentage'].max()
peak_time = hourly_data['occupancy_percentage'].idxmax()
low_usage_periods = hourly_data[hourly_data['occupancy_percentage'] < 20].shape[0]

print(f"Average Occupancy Percentage: {average_occupancy:.2f}%")
print(f"Peak Occupancy Percentage: {peak_occupancy:.2f}%")
print(f"Peak Time: {peak_time}")
print(f"Low Usage Periods (hours with less than 20% occupancy): {low_usage_periods}")
