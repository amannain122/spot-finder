import cv2
import numpy as np
from ultralytics import YOLO
import pafy
import csv
from datetime import datetime
import os

# Load the YOLO model
model = YOLO('yolov8x.pt')

# YouTube video URL
video_url = 'https://www.youtube.com/watch?v=HBDD3j5so0g'

# Set up video streaming
video = pafy.new(video_url)
best_stream = video.getbest(preftype="mp4")
cap = cv2.VideoCapture(best_stream.url)

# Define new bounding box areas with the provided coordinates
bounding_box_areas = [
    [(698, 605), (794, 558), (831, 569), (749, 622)],  # SP1
    [(759, 627), (868, 572), (910, 589), (812, 646)],  # SP2
    [(820, 651), (936, 587), (959, 596), (882, 673)],  # SP3
    [(888, 680), (1011, 615), (1064, 622), (962, 702)],  # SP4
    [(966, 707), (1099, 636), (1178, 673), (1049, 748)],  # SP5
    [(1168, 796), (1289, 707), (1401, 743), (1284, 842)],  # SP6
    [(1287, 856), (1408, 741), (1540, 792), (1450, 905)]  # SP7
]

# Initialize list to track if bounding boxes are empty or not
bounding_boxes_status = [False] * len(bounding_box_areas)
prev_empty_boxes = len(bounding_box_areas)

# Define CSV file path
csv_file_path = 'parking_status.csv'
file_exists = os.path.isfile(csv_file_path)

with open(csv_file_path, mode='a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    if not file_exists:
        csv_writer.writerow(['Timestamp', 'SP1', 'SP2', 'SP3', 'SP4', 'SP5', 'SP6', 'SP7'])

    # Loop through the video frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Predict using YOLO model
        results = model.predict(frame, verbose=False)
        detections = results[0].boxes.data

        # Extract the class names from the model
        class_names = model.names

        # Reset bounding boxes status
        bounding_boxes_status = [False] * len(bounding_box_areas)

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
                        bounding_boxes_status[i] = True
                        break
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Draw all bounding box areas and label them as SP1, SP2, etc.
        for i, area in enumerate(bounding_box_areas):
            cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 255, 255), 2)
            area_center = np.mean(area, axis=0).astype(int)
            cv2.putText(frame, f'SP{i + 1}', tuple(area_center), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        empty_boxes = bounding_boxes_status.count(False)

        # Print only when the empty_boxes value changes
        if empty_boxes != prev_empty_boxes:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status_row = [timestamp] + ['occupied' if status else 'empty' for status in bounding_boxes_status]
            csv_writer.writerow(status_row)
            print(f"Number of empty lots: {empty_boxes}")
            print(f"Number of occupied lots: {len(bounding_box_areas) - empty_boxes}")
            for i, status in enumerate(bounding_boxes_status):
                print(f"SP{i + 1} is {'occupied' if status else 'empty'}")
            prev_empty_boxes = empty_boxes

        # Display the frame
        cv2.imshow('Result', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release video capture and close CSV file
cap.release()
cv2.destroyAllWindows()
