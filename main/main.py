import cv2
import numpy as np
from ultralytics import YOLO
import yt_dlp
import pandas as pd
from datetime import datetime
from multiprocessing import Process, Lock
import os
from pathlib import Path

# Function to process each parking lot
def process_parking_lot(parking_lot_id, video_url, roi_csv_path, output_csv_path, lock, root_dir):
    # Load the YOLO model
    model_path = os.path.join(root_dir, 'src/models/yolov8n.pt')
    #model = YOLO('../src/models/yolov8n.pt')
    model = YOLO(model_path)
    
    # Read the ROI CSV file
    data = pd.read_csv(roi_csv_path)

    # Extract bounding box coordinates
    bounding_box_areas = []
    for i in range(len(data)):
        coords = [
            (data['Point1_X'].iloc[i], data['Point1_Y'].iloc[i]),
            (data['Point2_X'].iloc[i], data['Point2_Y'].iloc[i]),
            (data['Point3_X'].iloc[i], data['Point3_Y'].iloc[i]),
            (data['Point4_X'].iloc[i], data['Point4_Y'].iloc[i])
        ]
        bounding_box_areas.append(coords)

    # Set up video streaming
    ydl_opts = {
        'format': 'best[height=720]',
        'noplaylist': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_url = info_dict['url']
        cap = cv2.VideoCapture(video_url)
    except Exception as e:
        print(f"Error loading video for {parking_lot_id}: {e}")
        return

    # Initialize list to track if bounding boxes are empty or not
    bounding_boxes_status = ['empty'] * len(bounding_box_areas)
    prev_empty_boxes = len(bounding_box_areas)

    # Loop through the video frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Predict using YOLO model
        results = model.predict(frame, verbose=False)
        detections = results[0].boxes.data

        class_names = model.names

        # Reset bounding boxes status for this frame
        bounding_boxes_status = ['empty'] * len(bounding_box_areas)

        # Iterate through detections and check if 'car' or 'truck' is within any of the specified bounding box areas
        for detection in detections:
            x1, y1, x2, y2, confidence, class_id = map(int, detection[:6])
            class_name = class_names[class_id]

            if class_name in ['car', 'truck']:
                # Calculate the center of the bounding box
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Check if the center of the bounding box is inside any of the specified areas
                for i, area in enumerate(bounding_box_areas):
                    point_in_polygon = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)

                    # Draw bounding box and center point if the car or truck is within the specified area
                    if point_in_polygon >= 0:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
                        bounding_boxes_status[i] = 'occupied'
                        break
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Draw all bounding box areas
        for i, area in enumerate(bounding_box_areas):
            cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 255, 255), 2)
            area_center = np.mean(area, axis=0).astype(int)
            cv2.putText(frame, f'SP{i + 1}', tuple(area_center), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        empty_boxes = bounding_boxes_status.count('empty')

        # Print only when the empty_boxes value changes
        if empty_boxes != prev_empty_boxes:
            print(f"Number of empty lots for {parking_lot_id}: {empty_boxes}")
            print(f"Number of occupied lots for {parking_lot_id}: {len(bounding_box_areas) - empty_boxes}")
            for i, status in enumerate(bounding_boxes_status):
                print(f"{parking_lot_id} SP{i + 1} is {status}")

            # Write the data to the CSV file
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            row = [parking_lot_id, timestamp] + bounding_boxes_status

            # Use a lock to ensure no other process writes to the CSV file simultaneously
            with lock:
                try:
                    df = pd.read_csv(output_csv_path)
                    if parking_lot_id in df['ParkingLotID'].values:
                        # Find the index of the parking lot and update the row
                        index = df[df['ParkingLotID'] == parking_lot_id].index[0]
                        # Update only the status columns and timestamp
                        for i in range(len(bounding_boxes_status)):
                            df.loc[index, f'SP{i + 1}'] = bounding_boxes_status[i]
                        df.loc[index, 'Timestamp'] = timestamp
                    else:
                        # Create a new row with correct columns
                        new_df = pd.DataFrame([row], columns=['ParkingLotID', 'Timestamp'] + [f'SP{i + 1}' for i in range(len(bounding_box_areas))])
                        df = pd.concat([df, new_df], ignore_index=True)
                except FileNotFoundError:
                    # Create a new DataFrame if the file doesn't exist
                    df = pd.DataFrame([row], columns=['ParkingLotID', 'Timestamp'] + [f'SP{i + 1}' for i in range(len(bounding_box_areas))])

                # Write the DataFrame back to the CSV file
                df.to_csv(output_csv_path, index=False)

            prev_empty_boxes = empty_boxes

        # Display the frame (commented out for non-interactive environments)
        cv2.imshow('Result', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    # Release video capture
    cap.release()
    cv2.destroyAllWindows()

# Main function to read the parking_lots.csv and start processes
def main():

    root_dir = Path(__file__).resolve().parents[1]
    parking_lots_csv_path = os.path.join(root_dir, 'src/data/parking_lots.csv')
    output_csv_path = os.path.join(root_dir, 'src/data/parking_status.csv')

    # Read the parking lots CSV
    parking_lots_data = pd.read_csv(parking_lots_csv_path)

    processes = []
    lock = Lock()

    # Start a process for each parking lot
    for index, lot in parking_lots_data.iterrows():
        parking_lot_id = lot['ParkingLotID']
        video_url = lot['URL']
        roi_csv_path = os.path.join(root_dir, 'src/data', lot['ROI'])

        p = Process(target=process_parking_lot, args=(parking_lot_id, video_url, roi_csv_path, output_csv_path, lock, root_dir))
        p.start()
        processes.append(p)

    # Ensure all processes complete
    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
