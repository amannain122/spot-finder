#!/usr/bin/env python
# coding: utf-8

# In[210]:


#!pip install -q timm pycocotools scipy
#!pip install -qU pytorch-lightning transformers
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import DetrConfig, DetrForObjectDetection, DetrImageProcessor
import torchvision
from PIL import Image, ImageDraw
import os
import json


# In[211]:


base_path = "C:/Users/rooyv/Documents/Loyalist/TERM 2/STEP 2/NOTEBOOKS"
images_path = os.path.join(base_path, "DETR_Resources/Audi/car")
#annotations_path = os.path.join(base_path, "DETR_Resources")


# In[212]:


class CocoDetection(torchvision.datasets.CocoDetection):
    def __init__(self, img_folder, feature_extractor, train=True):
        ann_file = os.path.join(img_folder, "output_coco_annotations2.json" if train else "output_coco_annotations_val.json")
        super(CocoDetection, self).__init__(img_folder, ann_file)
        self.feature_extractor = feature_extractor

    def __getitem__(self, idx):
        # read in PIL image and target in COCO format
        img, target = super(CocoDetection, self).__getitem__(idx)
        
        # preprocess image and target (converting target to DETR format, resizing + normalization of both image and target)
        image_id = self.ids[idx]
        target = {'image_id': image_id, 'annotations': target}
        encoding = self.feature_extractor(images=img, annotations=target, return_tensors="pt")
        pixel_values = encoding["pixel_values"].squeeze() # remove batch dimension
        target = encoding["labels"][0] # remove batch dimension

        return pixel_values, target


# In[213]:


from transformers import DetrFeatureExtractor

img_folder = images_path

feature_extractor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")

train_dataset = CocoDetection(img_folder=f'{img_folder}/train', feature_extractor=feature_extractor)
val_dataset = CocoDetection(img_folder=f'{img_folder}/val', feature_extractor=feature_extractor, train=False)


# In[214]:


print("Number of training examples:", len(train_dataset))
print("Number of validation examples:", len(val_dataset))


# In[215]:


import numpy as np
import os
from PIL import Image, ImageDraw

# based on https://github.com/woctezuma/finetune-detr/blob/master/finetune_detr.ipynb
image_ids = train_dataset.coco.getImgIds()
# let's pick a random image
image_id = image_ids[np.random.randint(0, len(image_ids))]
print('Image n°{}'.format(image_id))
image = train_dataset.coco.loadImgs(image_id)[0]
image = Image.open(os.path.join(f'{img_folder}/train', image['file_name']))

annotations = train_dataset.coco.imgToAnns[image_id]
draw = ImageDraw.Draw(image, "RGBA")

cats = train_dataset.coco.cats
id2label = {k: v['name'] for k,v in cats.items()}

for annotation in annotations:
  box = annotation['bbox']
  class_idx = annotation['category_id']
  x,y,w,h = tuple(box)
  draw.rectangle((x,y,x+w,y+h), outline='red', width=1)
  draw.text((x, y), id2label[class_idx], fill='white')

image


# In[216]:


from torch.utils.data import DataLoader

def collate_fn(batch):
  pixel_values = [item[0] for item in batch]
  encoding = feature_extractor.pad(pixel_values, return_tensors="pt")
  labels = [item[1] for item in batch]
  batch = {}
  batch['pixel_values'] = encoding['pixel_values']
  batch['pixel_mask'] = encoding['pixel_mask']
  batch['labels'] = labels
  return batch

train_dataloader = DataLoader(train_dataset, collate_fn=collate_fn, batch_size=4, shuffle=True)
val_dataloader = DataLoader(val_dataset, collate_fn=collate_fn, batch_size=2)
batch = next(iter(train_dataloader))


# In[217]:


batch.keys()


# In[218]:


pixel_values, target = train_dataset[0]


# In[219]:


pixel_values.shape


# In[220]:


print(target)


# In[221]:


import pytorch_lightning as pl
from transformers import DetrConfig, DetrForObjectDetection
import torch

class Detr(pl.LightningModule):

     def __init__(self, lr, lr_backbone, weight_decay):
         super().__init__()
         # replace COCO classification head with custom head
         self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", 
                                                             num_labels=len(id2label),
                                                             ignore_mismatched_sizes=True)
         # see https://github.com/PyTorchLightning/pytorch-lightning/pull/1896
         self.lr = lr
         self.lr_backbone = lr_backbone
         self.weight_decay = weight_decay

     def forward(self, pixel_values, pixel_mask):
       outputs = self.model(pixel_values=pixel_values, pixel_mask=pixel_mask)

       return outputs
     
     def common_step(self, batch, batch_idx):
       pixel_values = batch["pixel_values"]
       pixel_mask = batch["pixel_mask"]
       labels = [{k: v.to(self.device) for k, v in t.items()} for t in batch["labels"]]

       outputs = self.model(pixel_values=pixel_values, pixel_mask=pixel_mask, labels=labels)

       loss = outputs.loss
       loss_dict = outputs.loss_dict

       return loss, loss_dict

     def training_step(self, batch, batch_idx):
        loss, loss_dict = self.common_step(batch, batch_idx)     
        # logs metrics for each training_step,
        # and the average across the epoch
        self.log("training_loss", loss)
        for k,v in loss_dict.items():
          self.log("train_" + k, v.item())

        return loss

     def validation_step(self, batch, batch_idx):
        loss, loss_dict = self.common_step(batch, batch_idx)     
        self.log("validation_loss", loss)
        for k,v in loss_dict.items():
          self.log("validation_" + k, v.item())

        return loss

     def configure_optimizers(self):
        param_dicts = [
              {"params": [p for n, p in self.named_parameters() if "backbone" not in n and p.requires_grad]},
              {
                  "params": [p for n, p in self.named_parameters() if "backbone" in n and p.requires_grad],
                  "lr": self.lr_backbone,
              },
        ]
        optimizer = torch.optim.AdamW(param_dicts, lr=self.lr,
                                  weight_decay=self.weight_decay)
        
        return optimizer

     def train_dataloader(self):
        return train_dataloader

     def val_dataloader(self):
        return val_dataloader



# In[222]:


model = Detr(lr=1e-4, lr_backbone=1e-5, weight_decay=1e-4)

outputs = model(pixel_values=batch['pixel_values'], pixel_mask=batch['pixel_mask'])


# In[223]:


outputs.logits.shape


# Training the model for max_step

# In[224]:


from pytorch_lightning import Trainer

# Specify GPU usage by using 'devices' and optionally 'accelerator' parameters
trainer = Trainer(max_steps=100, gradient_clip_val=0.1, devices=1, accelerator='gpu')
#trainer.fit(model)


# In[225]:


ckpt_path = "C:/Users/rooyv/Documents/Loyalist/TERM 2/STEP 2/NOTEBOOKS/detr_model.ckpt"
trainer.fit(model, ckpt_path=ckpt_path)


# In[226]:


get_ipython().system('nvidia-smi')


# In[227]:


get_ipython().system('git clone https://github.com/facebookresearch/detr.git')
get_ipython().run_line_magic('cd', 'detr')


# In[228]:


from datasets import get_coco_api_from_dataset

base_ds = get_coco_api_from_dataset(val_dataset) # this is actually just calling the coco attribute


# In[229]:


get_ipython().run_line_magic('cd', '..')


# In[230]:


from datasets.coco_eval import CocoEvaluator
from tqdm.notebook import tqdm

iou_types = ['bbox']
coco_evaluator = CocoEvaluator(base_ds, iou_types) # initialize evaluator with ground truths

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)
model.eval()

print("Running evaluation...")

for idx, batch in enumerate(tqdm(val_dataloader)):
    # get the inputs
    pixel_values = batch["pixel_values"].to(device)
    pixel_mask = batch["pixel_mask"].to(device)
    labels = [{k: v.to(device) for k, v in t.items()} for t in batch["labels"]] # these are in DETR format, resized + normalized

    # forward pass
    outputs = model.model(pixel_values=pixel_values, pixel_mask=pixel_mask)

    orig_target_sizes = torch.stack([target["orig_size"] for target in labels], dim=0)
    results = feature_extractor.post_process_object_detection(outputs=outputs, target_sizes=orig_target_sizes, threshold=0.) # convert outputs of model to COCO api
    res = {target['image_id'].item(): output for target, output in zip(labels, results)}
    coco_evaluator.update(res)

coco_evaluator.synchronize_between_processes()
coco_evaluator.accumulate()
coco_evaluator.summarize()


# In[231]:


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)
model.eval()


# In[256]:


import torch
import matplotlib.pyplot as plt

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    #b = out_bbox
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

def plot_results(pil_img, prob, boxes):
    #plt.figure(figsize=(16,10))
    #plt.imshow(pil_img)
    #plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    #ax = plt.gca()
    colors = COLORS * 100
    for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), colors):
        #ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
         #                          fill=False, color=c, linewidth=3))
        print(p)
        cl = p.argmax()
        print(cl)
        print(id2label)  # Check what keys are actually in your dictionary
        text = f'{id2label[cl.item()]}: {p[cl]:0.2f}'
        #ax.text(xmin, ymin, text, fontsize=15,
                #bbox=dict(facecolor='yellow', alpha=0.5))
    print(text)
    #plt.axis('off')
    #plt.show()


# In[264]:


import torchvision.ops as ops

def visualize_predictions(image, outputs, threshold=0.9, keep_highest_scoring_bbox=False, iou_threshold=0.5):  #iou low = less boxes
  # keep only predictions with confidence >= threshold
  probas = outputs.logits.softmax(-1)[0, :, :-1]

  scores = outputs['logits'].softmax(-1)
  labels = scores.argmax(-1)  # Get the predicted class indices
  #print(labels)
    
  keep = probas.max(-1).values > threshold
  #print(threshold)
  #print(probas.max(-1).values)
  if keep_highest_scoring_bbox:
    keep = probas.max(-1).values.argmax()
    keep = torch.tensor([keep])
  else:
      keep = torch.nonzero(keep).squeeze(1)

  if keep.numel() == 0:
    print("No bounding boxes with confidence above the threshold.")
    return
  #print(labels.tolist()[0][keep.item()])
  #class_idx = labels.tolist()[0][keep.item()]
  class_idx = labels[0, keep].tolist()
   #convert predicted boxes from [0; 1] to image scales
  boxes_scaled = rescale_bboxes(outputs.pred_boxes[0, keep].cpu(), image.size)
  boxes_scaled = boxes_scaled.to(device)

  # Apply non-maximum suppression
  probas_keep = probas.max(-1).values[keep]
  keep_nms = ops.nms(boxes_scaled, probas_keep, iou_threshold)
  keep = keep_nms

  boxes_scaled = boxes_scaled[keep].cpu()
  class_idx = [class_idx[i] for i in keep]
  # print(f"Number of probabilities: {len(probas[keep])}")
  # print(probas[keep])
  # print(f"Number of bounding boxes: {len(boxes_scaled)}")
  # print(f"Image size: {image.size}")
  # print(f"boxes_scaled: {boxes_scaled}")

  from PIL import ImageDraw
  draw = ImageDraw.Draw(image)

  for bbox, label in zip(boxes_scaled, class_idx):
      draw.rectangle(bbox.tolist(), outline='red', width=3)
      draw.text((bbox[0], bbox[1]), id2label[label], fill='white')
    
  # image.show()



# In[234]:


it = iter(range(1500))


# In[235]:


trainer.save_checkpoint("detr_model.ckpt")


# To evaluate images from validation dataset

# In[236]:


#We can use the image_id in target to know which image it is
#pixel_values, target = val_dataset[next(it)]
import random

# Get a random index from the validation dataset
random_idx = random.randint(0, len(val_dataset)-1)
print(random_idx)
# Fetch the image and target using the random index
pixel_values, target = val_dataset[random_idx]

pixel_values = pixel_values.unsqueeze(0).to(device)
print(pixel_values.shape)


# In[237]:


# forward pass to get class logits and bounding boxes
outputs = model(pixel_values=pixel_values, pixel_mask=None)


# In[238]:


image_id = target['image_id'].item()
print(image_id)
image = val_dataset.coco.loadImgs(image_id)[0]
image = Image.open(os.path.join(f'{img_folder}/val', image['file_name']))
print(image)
print("Output type:", type(outputs))
print("Number of detections:", len(outputs))
#print("Image shape:", image.shape)
logits = outputs.logits
pred_boxes = outputs.pred_boxes
#print(pred_boxes)


# In[239]:


try:
    visualize_predictions(image, outputs, threshold=0.3, keep_highest_scoring_bbox=True)
except Exception as e:
    print("Error in visualization:", e)


# https://www.kaggle.com/code/nouamane/fine-tuning-detr-for-license-plates-detection/notebook?scriptVersionId=83102158

# In[268]:


import torch
from torch.utils.data import Dataset, DataLoader
from transformers import DetrImageProcessor, DetrForObjectDetection
import os
from PIL import Image, ImageDraw

# Custom Dataset for Test Images
class TestDataset(Dataset):
    def __init__(self, img_folder, feature_extractor):
        self.img_folder = img_folder
        self.feature_extractor = feature_extractor
        self.img_files = [f for f in os.listdir(img_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_folder, self.img_files[idx])
        img = Image.open(img_path).convert("RGB")
        encoding = self.feature_extractor(images=img, return_tensors="pt")
        pixel_values = encoding["pixel_values"].squeeze(0).to(device)  # Keep batch dimension for DataLoader
        return pixel_values, self.img_files[idx]

# Load Test Dataset
test_img_folder = os.path.join(base_path, "DETR_Resources/Audi/car/test")
test_dataset = TestDataset(img_folder=test_img_folder, feature_extractor=feature_extractor)
test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers=0)

# Process each image in the test dataset
for pixel_values, img_file in test_dataloader:
    pixel_values = pixel_values.to(device)
    # forward pass to get class logits and bounding boxes
    outputs = model(pixel_values=pixel_values, pixel_mask=None)
    image_id = img_file[0].replace(".jpg", "").replace(".png", "").replace(".jpeg", "")
    print(f"Processing image: {image_id}")

    logits = outputs.logits
    pred_boxes = outputs.pred_boxes
    image_path = os.path.join(test_img_folder, img_file[0])
    image = Image.open(image_path)

    try:
        visualize_predictions(image, outputs, threshold=0.04, keep_highest_scoring_bbox=False, iou_threshold=0.3)
    except Exception as e:
        print(f"Error in visualization for image {image_id}: {e}")

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import DetrImageProcessor
import yt_dlp
import threading
import queue
import cProfile
import pstats
import io
from pstats import SortKey
import signal
import sys
import torchvision.ops as ops

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

profiler = cProfile.Profile()


def profile_function(func):
    """A simple decorator for profiling a function."""

    def wrapper(*args, **kwargs):
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
        ps.print_stats()
        with open("profiling_results.txt", "w") as f:
            f.write(s.getvalue())
        print(s.getvalue())
        return result

    return wrapper


def signal_handler(sig, frame):
    profiler.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    ps.print_stats()
    with open("profiling_results.txt", "w") as f:
        f.write(s.getvalue())
    print(s.getvalue())
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def process_frame(frame_queue, model, feature_extractor, processed_frame_queue):
    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        # Convert frame to PIL image
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Transform the image
        encoding = feature_extractor(images=img, return_tensors="pt")
        pixel_values = encoding["pixel_values"].squeeze(0).to(device)

        # Perform detection
        with torch.no_grad():
            outputs = model(pixel_values=pixel_values.unsqueeze(0), pixel_mask=None)

        # Visualize the results
        visualize_predictions(img, outputs, threshold=0.08, keep_highest_scoring_bbox=False, iou_threshold=0.5)

        # Convert PIL image back to frame
        processed_frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        processed_frame_queue.put(processed_frame)


@profile_function
def process_youtube_video(video_url, model, resolution='best[height<=480]', frame_skip=5, num_threads=10):
    ydl_opts = {
        'format': resolution,  # Adjust to desired resolution
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_url = info_dict['url']
        print("Video URL:", video_url)  # Debug: Print the video URL

    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        print("Error: Unable to open video stream.")
        return

    feature_extractor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    frame_queue = queue.Queue(maxsize=10)
    processed_frame_queue = queue.Queue(maxsize=10)

    # Create multiple processing threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=process_frame, args=(frame_queue, model, feature_extractor, processed_frame_queue))
        t.start()
        threads.append(t)

    frame_count = 0
    stop_flag = False

    while cap.isOpened() and not stop_flag:
        ret, frame = cap.read()
        if not ret:
            print("Error: Frame not read properly.")
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        if frame_queue.full():
            continue

        frame_queue.put(frame)

        if not processed_frame_queue.empty():
            processed_frame = processed_frame_queue.get()
            cv2.imshow('Live Stream', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_flag = True
            break

    for _ in range(num_threads):
        frame_queue.put(None)

    for t in threads:
        t.join()

    cap.release()
    cv2.destroyAllWindows()


# URL of the YouTube live video
youtube_url = 'https://www.youtube.com/watch?v=QH0z-Dx6s7c'

# Assuming 'model' is already defined and loaded
process_youtube_video(youtube_url, model, resolution='best[height<=480]', frame_skip=5, num_threads=10)





