#In order to run this code you need to clone the YOLO GIT from git clone https://github.com/THU-MIG/YOLOV10.git

import cv2
import numpy as np
from ultralytics import YOLOv10
import pafy
from yt_dlp import YoutubeDL

# Load the YOLO model with custom weights
custom_weights_path ="C://Users//rooyv//Documents//Loyalist//TERM 2//STEP 2//Saraka//runs//detect//train6//weights//best.pt"
model = YOLOv10(custom_weights_path)

# YouTube video URL
video_url = 'https://www.youtube.com/watch?v=HBDD3j5so0g'

# Set up video streaming
video = pafy.new(video_url)
best_stream = video.getbest(preftype="mp4")
cap = cv2.VideoCapture(best_stream.url)

# Define new bounding box areas with the provided coordinates
bounding_box_areas = [
    [(698, 605), (794, 558), (831, 569), (749, 622)],      # SP1
    [(759, 627), (868, 572), (910, 589), (812, 646)],      # SP2
    [(820, 651), (936, 587), (959, 596), (882, 673)],      # SP3
    [(888, 680), (1011, 615), (1064, 622), (962, 702)],    # SP4
    [(966, 707), (1099, 636), (1178, 673), (1049, 748)],   # SP5
    [(1168, 796), (1289, 707), (1401, 743), (1284, 842)],  # SP6
    [(1287, 856), (1408, 741), (1540, 792), (1450, 905)]   # SP7
]

# Initialize list to track if bounding boxes are empty or not
bounding_boxes_status = [False] * len(bounding_box_areas)
prev_empty_boxes = len(bounding_box_areas)

# Loop through the video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Print frame details
    print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}")

    # Predict using YOLO model
    results = model.predict(frame, verbose=False)
    
    # Check and print results directly
    #if not results:
    #    print("No detections made by the model.")
    #    continue

    detections = results[0].boxes.data
    print(f"Detections: {detections}")

    # Check if there are any detections
    #if detections.shape[0] == 0:
    #    print("No objects detected in the current frame.")
    #    continue

    # Extract the class names from the model
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

    # Draw all bounding box areas and label them as SP1, SP2, etc.
    for i, area in enumerate(bounding_box_areas):
        cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 0), 2)
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
