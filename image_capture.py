#Script to capture train images
#Need jpeg library and Python Image Library (PIL)

#JPEG libraries
#get here: http://arcoleo.org/dsawiki/Wiki.jsp?page=How%20to%20Install%20Libjpeg%20on%20Mac
#OR if you have homebrew, just type into command line brew install libjpeg  
#To verify, this library should be in /usr/local/lib after install

#Python Image Library
#Get this here: http://pythonware.com/products/pil/
#Unzip, go into Downloads folder and run the following command to edit (note that CTRL X will exit edit mode): nano setup.py
#Change jpeg = NONE to jpeg=/usr/local/lib  
#Run in command line: sudo python setup.py install  

#This script does the following:
#Captures images from a traffic camera every 1 second up to 15 minutes. 
#Crops image for section with train (assumes train is on the left)
#Saves image to local drive

#Note - public token in image URL changes about every 15 minutes, so you can only use the current public token for 15 min
import urllib
import Image
import time

from urllib import urlretrieve

for i in range(1, 900):
	urllib.urlretrieve("http://pub2.camera.trafficland.com/image/live.jpg?system=santaclara&webid=401848&size=full&pubtoken=2880d7bf2c91858c1e41df558cfece5a&1389117451002", "test.jpg")
	img=Image.open('test.jpg')
	img=img.crop((0,0,100,240))
	index = i
	jpg_string=".jpg"
	imfile=str(index)+jpg_string
	img.save(imfile)
	time.sleep(1) 
