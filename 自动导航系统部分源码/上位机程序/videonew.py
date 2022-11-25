# coding=utf-8
import os
import sys
import cv2
import math
import socket
import numpy as np
from mrcnn.config import Config
from datetime import datetime
import serial
import pynmea2

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
# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_yumi2_0006.h5")

w1 = 'yes'
w2 = 'no'
w3=116.3499066
w4=40.0049290

def Love(inputdata):
    global w1
    global w2
    global w3
    global w4
	ser = serial.Serial(inputdata, '38400', timeout=0.5)
	print(ser.is_open)
	datahex = ser.readline()
	datahex = str(datahex, encoding='utf-8')
	if datahex.startswith('$GNRMC'):
		rmc=pynmea2.parse(datahex)
        if (len(str(rmc.latitude).split(".")[1]) >= 14) and (len(str(rmc.longitude).split(".")[1]) >= 14):
            a = round(rmc.latitude,7)
            b = round(rmc.longitude,7)
            if (abs(a-w3)<=4e-7)and(abs(b-w4)<=4e-7):
                return w1
            else:
                return w2
            # print("Latitude:",round(rmc.latitude,6))
            # print("Longitude:",round(rmc.longitude,6))

class ShapesConfig(Config):
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

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

class_names = ['BG', 'yumi']

class Pid():
	def __init__(self, exp_val, kp, ki, kd, ne, le, lle):
		self.KP = kp
		self.KI = ki
		self.KD = kd
		self.exp_val = exp_val
		self.now_val = 0
		self.now_err = ne
		self.last_err = le
		self.last_last_err = lle
		self.change_val = 0

	def cmd_pid(self):
		self.last_last_err = self.last_err
		self.last_err = self.now_err
		self.now_err = self.exp_val - self.now_val
		self.change_val = self.KP * (self.now_err - self.last_err) + self.KI * \
			self.now_err + self.KD * (self.now_err - 2 * self.last_err
									  + self.last_last_err)
		#print(self.change_val)
		self.now_val += self.change_val
		return self.now_val

s = socket.socket()
s.bind(("192.168.199.221",8282)) # 绑定地址和端口
s.listen(1)           # 等待客户端连接，连接数为参数
c,addr = s.accept()   # 建立客户端连接
print("与"+str(addr)+"建立了连接")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
fx = 391.9784
fy = 391.7699
u0 = 324.7212
v0 = 271.4266
h = 81.0000
time = 0
pid_val = []
#sp = (480,640,3)

# for cishu in range(5):
# 	c.send(str.encode("W"))
# 	data = c.recv(1024)
# 	if data == str.encode("T"):
# 		print(data)
# 		break

while True:
	time+=1
	ret, frame = cap.read()

	if time == 12:
		for cishu in range(5):
			c.send(str.encode("W"))

	if time % 4 == 0:
		#a = datetime.now()
		#image = frame
		#image = cv2.resize(frame, (480, 360))
		image = frame
		results = model.detect([image], verbose=1)
		r = results[0]
		mask = r['masks']
		c = []
		collector = []
		for i in range(260, 380, 4):
			for j in range(10, 630):
				if len(c) == 8:
					heng = int((c[2] + c[3] + c[4] + c[5]) / 4)
					zhong = int(i)
					#pic = cv2.circle(image, (heng, zhong), 2, (0, 255, 255), -1)
					# pic = cv2.circle(image, (heng1, zhong), 2, (2, 0, 244), -1)
					# pic = cv2.circle(image, (heng2, zhong), 2, (2, 0, 244), -1)
					# print(zhong)
					collector.append([heng, zhong])
					c.clear()
					break
				if (mask[i][j - 1] == True) and (mask[i][j + 1] == False):
					c = c + [j]
				elif (mask[i][j - 1] == False) and (mask[i][j + 1] == True):
					c = c + [j]
		#b = datetime.now()
		#print('shijian', b - a)
		for q in collector:
			if q[0] < 200 or q[0] > 440:
				collector.remove(q)
		dot_collector = np.array(collector)
		output = cv2.fitLine(dot_collector, cv2.DIST_L12, 0, 0.01, 0.01)
		k = -100 * (output[1] / output[0])
        y = output[3] - k * output[2]

		b = y[0]
		S = math.cos(30)*(v0-k*u0-b)-fy*math.sin(30)
		S = S[0]
		T = math.sin(30)*(h*k*u0+h*b-v0*h)-fy*h*math.cos(30)
		T = T[0]
		K = (2*k*fx)/S
		K = -K[0]
		B = T/S
		#print(K,B)

		g = B/((1+K**2)**0.5)
		g = -int(g)
		j = math.degrees(math.atan(K))/3
		j = int(j)
		#b = datetime.now()
		print(g,j)
		pid_val.append(j)
		print(pid_val)
		geshu = len(pid_val)
		if time == 12:
			my_Pid = Pid(29, 100, 30, 5, abs(j), 0, 0)
			t = my_Pid.cmd_pid()
		elif time == 16:
			a1 = pid_val[geshu-2]
			a1 = abs(a1)
			my_Pid = Pid(29, 100, 30, 5, abs(j), a1, 0)
			t = my_Pid.cmd_pid()
		elif time == 20:
			a1 = pid_val[geshu-2]
			a2 = pid_val[geshu-3]
			a1 = abs(a1)
			a2 = abs(a2)
			my_Pid = Pid(29, 100, 30, 5, abs(j), a1, a2)
			t = my_Pid.cmd_pid()
		elif time > 20:
			a1 = pid_val[geshu - 2]
			a2 = pid_val[geshu - 3]
			a1 = abs(a1)
			a2 = abs(a2)
			my_Pid = Pid(29, 100, 30, 5, abs(j), a1, a2)
			t = my_Pid.cmd_pid()

		if (j > 0) and (g<0) and (abs(g) > 2) and (abs(j) < 29) and (time>8):
			while True:
				c.send(str.encode("Z"))
				data = c.recv(1024)
				if data == str.encode("O"):#确定小车收到左转命令
					while True:
						t = int(abs(t))
						t = str(t)
						print(t)
						c.send(str.encode(t))
						datas = c.recv(1024)
						if datas == str.encode("M"):
							break
					break

		if (j < 0) and (g<0) and (abs(g) > 3) and (abs(j) < 29) and (time>8):
			while True:
				c.send(str.encode("Y"))
				data = c.recv(1024)
				if data == str.encode("O"):
					while True:
						t = int(abs(t))
						t = str(t)
						print(t)
						c.send(str.encode(t))
						datas = c.recv(1024)
						if datas == str.encode("N"):
							break
					break

		if Love(com11) == 'yes':
			while True:
				c.send(str.encode("S"))
				datas = c.recv(1024)
				if datas == str.encode("L"):
					break


