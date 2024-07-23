from ultralytics import YOLO

model = YOLO('yolov8x.pt')

model.predict("Screenshot (17).png")