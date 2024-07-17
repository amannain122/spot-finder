import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import time
import os
import matplotlib.pyplot as plt

# Local path to the video file on the desktop
# change the path url for Windows
LOCAL_VIDEO_FILE = "/Users/tinaukanwune/Desktop/parking1 2.mp4" 

# Create a VideoCapture object with the local video file
cap = cv2.VideoCapture(LOCAL_VIDEO_FILE)
if not cap.isOpened():
    print(f"Error: Could not open video file '{LOCAL_VIDEO_FILE}'.")
    exit()

# Initialize background subtractor
back_sub = cv2.createBackgroundSubtractorMOG2()

# Initialize heat map
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame or end of video.")
    cap.release()
    cv2.destroyAllWindows()
    exit()
heat_map = np.zeros_like(frame, dtype=np.float32)

# Lists to store data for plotting
timestamps = []
occupancy_percentages = []


# Function to detect occupied areas
def detect_occupied_areas(frame):
    fg_mask = back_sub.apply(frame)
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    occupied_areas = []
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area to filter noise
            x, y, w, h = cv2.boundingRect(contour)
            occupied_areas.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame, occupied_areas


# Function to calculate occupancy percentage
def calculate_occupancy(occupied_areas, frame_shape):
    total_parking_lot_area = frame_shape[0] * frame_shape[1]
    occupied_area = sum([w * h for (x, y, w, h) in occupied_areas])
    occupancy_percentage = (occupied_area / total_parking_lot_area) * 100
    return occupancy_percentage


# Function to save occupancy data to CSV
def save_occupancy_data(timestamp, occupancy_percentage, csv_file):
    data = {"timestamp": timestamp, "occupancy_percentage": occupancy_percentage}
    df = pd.DataFrame([data])
    df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)


# Function to plot occupancy over time
def plot_occupancy(timestamps, occupancy_percentages):
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, occupancy_percentages, marker='o', linestyle='-', color='b')
    plt.title('Occupancy Percentage Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Occupancy Percentage (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("/Users/tinaukanwune/Desktop/spotfinder/occupancy_plot.png")  # Save plot as PNG
    plt.show()


# Specify the CSV file path
csv_file = "/Users/tinaukanwune/Desktop/spotfinder/occupancy_data.csv"

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["timestamp", "occupancy_percentage"]).to_csv(csv_file, index=False)

# Timer to save occupancy data and plot every second
start_time = time.time()
end_time = start_time + 3600  # Run for 1 hour

while cap.isOpened() and time.time() < end_time:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame or end of video.")
        break

    frame, occupied_areas = detect_occupied_areas(frame)
    occupancy_percentage = calculate_occupancy(occupied_areas, frame.shape)

    for (x, y, w, h) in occupied_areas:
        heat_map[y:y + h, x:x + w] += 1  # Increase the heat in the occupied area

    heat_map_normalized = cv2.normalize(heat_map, None, 0, 255, cv2.NORM_MINMAX)
    heat_map_colored = cv2.applyColorMap(heat_map_normalized.astype(np.uint8), cv2.COLORMAP_JET)
    combined = cv2.addWeighted(frame, 0.7, heat_map_colored, 0.3, 0)

    cv2.putText(combined, f'Occupancy: {occupancy_percentage:.2f}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                2)
    cv2.imshow('Parking Lot Heat Map', combined)

    # Save occupancy data and plot every second
    current_time = time.time()
    if current_time - start_time >= 1:
        timestamps.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        occupancy_percentages.append(occupancy_percentage)

        save_occupancy_data(timestamps[-1], occupancy_percentage, csv_file)

        plot_occupancy(timestamps, occupancy_percentages)

        start_time = current_time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
