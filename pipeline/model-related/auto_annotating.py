import os
import json
import torch
from PIL import Image
from pycocotools.coco import COCO

# Function to create COCO-style annotations
def create_coco_annotation(annotation_id, image_id, bbox, category_id=1):
    return {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "bbox": bbox,
        "area": bbox[2] * bbox[3],
        "segmentation": [],
        "iscrowd": 0
    }

def get_image_info(file_name, image_id):
    image = Image.open(file_name)
    width, height = image.size
    return {
        "id": image_id,
        "file_name": file_name,
        "width": width,
        "height": height
    }

def main():
    image_folder = "red_cars"
    annotation_file = "annotations.json"
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    coco_output = {
        "info": {
            "description": "Red Car Dataset",
            "version": "1.0",
            "year": 2024
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": [
            {
                "id": 1,
                "name": "car",
                "supercategory": "vehicle"
            }
        ]
    }

    image_id = 1
    annotation_id = 1

    for image_file in os.listdir(image_folder):
        if image_file.endswith(".jpg"):
            image_path = os.path.join(image_folder, image_file)
            img = Image.open(image_path)
            results = model(img, size=640)

            image_info = get_image_info(image_path, image_id)
            coco_output["images"].append(image_info)

            for *xyxy, conf, cls in results.xyxy[0].cpu().numpy():
                if int(cls) == 2:  # COCO class index for 'car'
                    x_min, y_min, x_max, y_max = map(int, xyxy)
                    bbox = [x_min, y_min, x_max - x_min, y_max - y_min]
                    annotation = create_coco_annotation(annotation_id, image_id, bbox)
                    coco_output["annotations"].append(annotation)
                    annotation_id += 1

            image_id += 1

    with open(annotation_file, 'w') as f:
        json.dump(coco_output, f, indent=4)

    print(f"Annotations saved to {annotation_file}")

if __name__ == "__main__":
    main()