import cv2
import numpy as np
from ultralytics import YOLO
import pafy
import pandas as pd

# Load the YOLO model
model = YOLO('yolov8x.pt')

video_url = 'https://www.youtube.com/watch?v=HBDD3j5so0g'

csv_path = 'rois.csv'
data = pd.read_csv(csv_path)

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
try:
    video = pafy.new(video_url)
    streams = video.streams

    desired_resolution = "1280x720"
    stream = next((s for s in video.streams if s.resolution == desired_resolution), None)
    if stream is None:
        print(f"Desired resolution {desired_resolution} not found. Falling back to the best available stream.")
        stream = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(stream.url)
except Exception as e:
    print(f"Error loading video: {e}")
    exit()

# Initialize list to track if bounding boxes are empty or not
bounding_boxes_status = [False] * len(bounding_box_areas)
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

    # Draw all bounding box areas
    for i, area in enumerate(bounding_box_areas):
        cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 255, 255), 2)
        area_center = np.mean(area, axis=0).astype(int)
        cv2.putText(frame, f'SP{i+1}', tuple(area_center), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    empty_boxes = bounding_boxes_status.count(False)

    # Print only when the empty_boxes value changes
    if empty_boxes != prev_empty_boxes:
        print(f"Number of empty lots: {empty_boxes}")
        print(f"Number of occupied lots: {len(bounding_box_areas) - empty_boxes}")
        for i, status in enumerate(bounding_boxes_status):
            print(f"SP{i+1} is {'occupied' if status else 'empty'}")
        prev_empty_boxes = empty_boxes

    # Display the frame
    cv2.imshow('Result', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture
cap.release()
cv2.destroyAllWindows()