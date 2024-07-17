#!/usr/bin/env python
# coding: utf-8

# In[16]:


get_ipython().system('python --version')


# In[17]:


get_ipython().system('git clone https://github.com/THU-MIG/YOLOV10.git')


# In[1]:


cd yolov10


# In[19]:


get_ipython().system('pip install .')


# In[2]:


import requests
import os
import urllib.request


# In[3]:


#base_path = "C:/Users/rooyv/Documents/Loyalist/TERM 2/STEP 2"
#images_path = os.path.join(base_path, "YOLO RO/images/Test")
#home_weights_path = "C:/Users/rooyv/Documents/Loyalist/TERM 2/STEP 2/YOLO RO/weights"

weights_dir = os.path.join(os.getcwd(),"weights")
os.makedirs(weights_dir,exist_ok=True)


# In[25]:


weights_dir = os.path.join(os.getcwd(),"weights")
os.makedirs(weights_dir,exist_ok=True)

urls = [
    "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10n.pt",
    "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10s.pt",
    "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10m.pt",
    "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10b.pt",
    "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10x.pt",
    "https://github.com/jameslahm/yolov10/releases/download/v1.0/yolov10l.pt"
]

for url in urls:
    file_name = os.path.join(weights_dir, os.path.basename(url))
    urllib.request.urlretrieve(url,file_name)
    print(f"Downloaded {file_name}")


# In[27]:


get_ipython().system('yolo task=detect mode=predict conf=0.25 save=True model=../weights/yolov10n.pt source=test_images/1.jpg')


# In[4]:


os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


# In[5]:


get_ipython().system('yolo task=detect mode=train epochs=25 batch=4 plots=True model=weights/yolov10n.pt data=custom_data.yaml')


# In[18]:


get_ipython().system('yolo task=detect mode=predict conf=0.2 save=True model=runs/detect/train5/weights/best.pt source=test_images/2.jpg nms=True iou=0.5')


# In[19]:
