##Script to capture images from camera on balcony and identify if there's a train

import urllib
import Image
import time
import cv2, cv
import numpy as np
import os, os.path
import scipy
import Image  

from urllib import urlretrieve
from scipy import mean, std
temp=list()
for i in range(0, 300):
	urllib.urlretrieve("http://svds-train-cam-1.svds.local:1026/snapshot.cgi", "pic1.jpg")
	img1=cv2.imread("pic1.jpg")
	urllib.urlretrieve("http://svds-train-cam-1.svds.local:1026/snapshot.cgi", "pic2.jpg")
	img2=cv2.imread("pic2.jpg")
	result=cv2.matchTemplate(img1, img2, cv2.TM_CCORR_NORMED)
	final=np.amax(result)
	temp.append(final)
	cnt=i
	if cnt>30:
		thres=mean(temp[i-30:i])-3*std(temp[i-30:i])
	else:
		thres=0.95
	if temp[i]<thres:
		print("TRAIN!!")
		index=i
		index2=i+1
		jpg_string=".jpg"
		img1=Image.open("pic1.jpg")
		img2=Image.open("pic2.jpg")
		imfile1=str(index)+jpg_string
		imfile2=str(index2)+jpg_string
		img1.save(imfile1)
		img2.save(imfile2)
	else:
		cnt=cnt 
