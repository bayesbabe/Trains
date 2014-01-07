#script to calculate and store normalized diff between consecutive images
#run script in directory with saved train images from image_capture.py

import Image
import numpy as np
import scipy
import os, os.path

from scipy.linalg import norm


N=len([name for name in os.listdir('.') if os.path.isfile(name)])-2 #number of train saved train pics... minus 2 subtracts counted directory and minus test.jpg (uncropped image)
jpg_string=".jpg"
temp=list()
for i in range(1, N):
	index1=i
	index2=i+1
	imfile1=str(index1)+jpg_string
	imfile2=str(index2)+jpg_string
	img1=Image.open(imfile1)
	img2=Image.open(imfile2)
	hist1=img1.histogram()
	hist2=img2.histogram()
	hist1=np.asarray(hist1)
	hist2=np.asarray(hist2)
	normdiff=1-np.linalg.norm(hist2-hist1)/np.linalg.norm(hist2+hist1)
	temp.append(round(normdiff,2))
