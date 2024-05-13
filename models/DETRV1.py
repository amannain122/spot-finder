import torch
from torch.utils.data import Dataset, DataLoader
from transformers import DetrConfig, DetrForObjectDetection, DetrImageProcessor
from PIL import Image
import os
import json
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from google.colab import drive
drive.mount('/content/drive')

images_path = "/content/drive/My Drive/Colab Notebooks/DETR_Resources/Audi/car"
annotations_path = "/content/drive/My Drive/Colab Notebooks/DETR_Resources/output_coco_annotations2.json"

# Initialize the processor from the DETR model
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

class ParkingSpotDataset(Dataset):
'''
This returns a dictionary with the pixels values, bbox and class
'''

    def __init__(self, annotations_file, img_dir, processor):
        self.img_dir = img_dir
        self.processor = processor
        with open(annotations_file) as f:
            self.data = json.load(f)

        # Group annotations by image_id
        self.grouped_annotations = {}
        for annotation in self.data['annotations']:
            image_id = annotation['image_id']
            if image_id not in self.grouped_annotations:
                self.grouped_annotations[image_id] = []
            self.grouped_annotations[image_id].append(annotation)

        self.images = self.data['images']

    def __getitem__(self, idx):
        image_info = self.images[idx]
        image_id = image_info['id']
        image_path = os.path.join(self.img_dir, image_info['file_name'])
        image = Image.open(image_path).convert("RGB")

        annotations = self.grouped_annotations.get(image_id, [])
        boxes = []
        labels = []
        for annotation in annotations:
            x_min, y_min, width, height = annotation['bbox']
            x_max = x_min + width
            y_max = y_min + height
            boxes.append([x_min, y_min, x_max, y_max])
            labels.append(annotation['category_id'])

        #print(f"Image ID {image_id} has {len(annotations)} annotations")  # Logging the number of annotations

        boxes = torch.tensor(boxes, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.long)

        # Resize the image
        resize_size = 800
        image = image.resize((resize_size, resize_size))
        processed = self.processor(image, return_tensors="pt")

        return {
            'pixel_values': processed['pixel_values'][0],  # Extract tensor
            'labels': {
                'boxes': boxes,
                'class_labels': labels
            }
        }

    def __len__(self):
        return len(self.images)


# Load the dataset and data loader
dataset = ParkingSpotDataset(annotations_path, images_path, processor)

# Load the pre-trained configuration and modify
num_custom_classes = 1
config = DetrConfig.from_pretrained("facebook/detr-resnet-50", num_labels=num_custom_classes + 1, revision="no_timm")  # +1 for the background class
model = DetrForObjectDetection(config)

# Training loop
optimizer = AdamW(model.parameters(), lr=5e-5)
model.train()
num_epochs = 1
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # Move model to the specified device
print("Using device:", device)

from torch.utils.data.dataloader import default_collate

def collate_fn(batch):
    """
    Custom collation function that properly handles batches of images with different numbers of annotations.
    """
    batch = {key: [d[key] for d in batch] for key in batch[0]}
    batch['pixel_values'] = default_collate(batch['pixel_values'])
    # Handle variable number of annotations per image
    batch['labels'] = {
        'boxes': [item['boxes'] for item in batch['labels']],  # List of tensors, one per batch item
        'class_labels': [item['class_labels'] for item in batch['labels']]  # List of tensors, one per batch item
    }
    return batch

# Using the custom collation function in DataLoader
dataloader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=collate_fn)

# Adjusted training loop
for epoch in range(num_epochs):
    for batch in dataloader:
        inputs = batch['pixel_values'].to(device)
        targets = []
        for i in range(inputs.shape[0]):
            targets.append({
                'boxes': batch['labels']['boxes'][i].to(device),
                'class_labels': batch['labels']['class_labels'][i].to(device)
            })

            #print(f"Input shape: {inputs.shape}")
            #print(f"Target {i} boxes shape: {targets[i]['boxes'].shape}")
            #print(f"Target {i} labels shape: {targets[i]['class_labels'].shape}")

        # Forward pass
        outputs = model(pixel_values=inputs, labels=targets)
        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Save the model's state dictionary
torch.save(model.state_dict(), '/content/drive/My Drive/Colab Notebooks/DETR_Resources/saved_model.pth')

