# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import skimage.io
import cv2
from mrcnn.config import Config
from datetime import datetime

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
#print(MODEL_DIR)
# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_yumi2_0006.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)
    print("Holdon***********************")

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images/new/")

class ShapesConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "shapes"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # background + 3 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    IMAGE_MIN_DIM = 320
    IMAGE_MAX_DIM = 384

    # Use smaller anchors because our image and objects are small
    RPN_ANCHOR_SCALES = (8 * 6, 16 * 6, 32 * 6, 64 * 6, 128 * 6)  # anchor side in pixels

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE =30

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = 50

    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 5

class InferenceConfig(ShapesConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Create model object in inference mode.
#model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

class_names = ['BG', 'yumi']
# Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
image = skimage.io.imread(os.path.join(IMAGE_DIR, "13.png"))
original=cv2.imread('E:/CODEWYL/MASK/Mask_RCNN-master/Mask_RCNN-master/images/new/13.png')
a=datetime.now()

results = model.detect([image], verbose=1)

r = results[0]

#visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])

mask=r['masks']
#print(mask)
#print(mask[0][1])
#gao=len(mask)
#kuan=len(mask[0])
#sp=(480, 640, 3)
c=[]
collector=[]
for i in range(240,400,4):
    for j in range(1,639):
        if len(c)==7:
            heng=int((c[3]+c[4])/2)
            heng1=int((c[1]+c[2])/2)
            heng2=int((c[5]+c[6])/2)
            zhong=int(i)
            pic = cv2.circle(original, (heng, zhong), 3, (0, 255, 255), -1)
            pic = cv2.circle(original, (heng1, zhong), 3, (2, 0, 244), -1)
            pic = cv2.circle(original, (heng2,zhong), 3, (2, 0, 244), -1)
            collector.append([heng, zhong])
            c.clear()
            break
        if (mask[i][j-1]==True) and (mask[i][j+1]==False):
            c=c+[j]
        elif (mask[i][j-1]==False) and (mask[i][j+1]==True):
            c=c+[j]
print(collector)
print(collector[0])
print(collector[0][0])
dot_collector=np.array(collector)

output = cv2.fitLine(dot_collector, cv2.DIST_L2, 0, 0.01, 0.01)

k=-100*(output[1]/output[0])
y=output[3] - k * output[2]
x=-y/k
#x=(sp[1]-output[3])/k+output[2]
# y=k*(0-output[2])+output[3]
# x=(sp[1]-output[3])/k+output[2]	#前面我们有了图像的大小，刚好可以求截距，这样有了两个点，就可以画直线了
# ptStart = (0,y)
# ptEnd = (x, sp[1])
#print(x,y,k)						#前面我们有了图像的大小，刚好可以求截距，这样有了两个点，就可以画直线了
ptStart = (x+10,0)
ptEnd = ((480-y)/k+30,480)
point_color = (255, 0, 0) #BGR
thickness = 4
lineType = 4
nihe=cv2.line(pic, ptStart, ptEnd, point_color, thickness, lineType)
b=datetime.now()
print('shijian',(b-a))
cv2.imshow('result', nihe)
cv2.imwrite('E:/CODEWYL/MASK/Mask_RCNN-master/Mask_RCNN-master/images/new/132.jpg',nihe)

cv2.waitKey(0)
cv2.destroyAllWindows()



