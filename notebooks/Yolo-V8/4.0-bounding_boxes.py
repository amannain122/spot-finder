import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8x.pt')

image_path = 'SSTest.png'
frame = cv2.imread(image_path)

bounding_box_areas = [
    [(1293, 906), (1450, 957), (1540, 845), (1414, 801)],  # SP1
    [(698, 666), (740, 686), (850, 643), (796, 622)],  # SP2
    [(816, 712), (945, 653), (1017, 678), (886, 740)],     # SP3
    [(886, 741), (1023, 679), (960, 770), (1102, 705)],    # SP4
    [(962, 774), (1100, 704), (1185, 732), (1049, 816)]    # SP5
]

bounding_boxes_status = [False] * len(bounding_box_areas)

results = model.predict(frame)
detections = results[0].boxes.data

class_names = model.names

for detection in detections:
    x1, y1, x2, y2, confidence, class_id = map(int, detection[:6])
    class_name = class_names[class_id]

    if class_name in ['car', 'truck']:
        # Calc center of the bounding box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

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

for i, area in enumerate(bounding_box_areas):
    cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 0), 2)
    area_center = np.mean(area, axis=0).astype(int)
    cv2.putText(frame, f'SP{i+1}', tuple(area_center), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

empty_boxes = bounding_boxes_status.count(False)
non_empty_boxes = bounding_boxes_status.count(True)

print(f"Number of empty lots: {empty_boxes}")
print(f"Number of occupied lots: {non_empty_boxes}")

for i, status in enumerate(bounding_boxes_status):
    print(f"SP{i+1} is {'occupied' if status else 'empty'}")

cv2.imshow('Result', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
