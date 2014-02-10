##Updated "is there a train" script - function for identifying a train is now a function of time - script will run for the specified amount of time or forever
##Needed libraries
import cv2
import numpy as np
import os, os.path 
import time, datetime
import glob
import shutil ##library to move files to folder

###Useful functions
def lmin(tslist, minute): #takes in current timestamp (as list) and current minute and finds the previous minute
	if minute==0:
		lastmin=str(59)
	else:
		lastmin=str(minute-1)
	return lastmin

def lsec(tslist, second): #takes in current timestamp (as list) and current second and finds the previous second
	if second==0:
		lastsec=str(59)
	else:
		lastsec=str(second-1)
	return lastsec

def tsdelay(tslist, lastmin, lastsec): #takes in current timestamp (as list), last minute, and last second, and creates string timestamps for the 2 images to be compared (prev min and prev 61 secs)
	if int(lastmin)<10 and int(lastsec)<10:
		ts1=tslist[0]+":"+"0"+lastmin+":"+tslist[2]
		ts2=tslist[0]+":"+"0"+lastmin+":"+"0"+lastsec
	else:
		if int(lastmin)<10 and int(lastsec)>9:
			ts1=tslist[0]+":"+"0"+lastmin+":"+tslist[2]
			ts2=tslist[0]+":"+"0"+lastmin+":"+lastsec
		else:
			if int(lastmin)>9 and int(lastsec)<10:
				ts1=tslist[0]+":"+lastmin+":"+tslist[2]
				ts2=tslist[0]+":"+lastmin+":"+"0"+lastsec
			else:
				ts1=tslist[0]+":"+lastmin+":"+tslist[2]
				ts2=tslist[0]+":"+lastmin+":"+lastsec
	return ts1, ts2

def getfiles(ts): #Grabs all files with ts string (string must end in asterisk)
	filelist=list()
	for file in glob.glob(ts):
		filelist.append(file)
	return filelist

def thres(diffs): #calculates threshold for image differences to identify a train
	if len(diffs)<30:
		thres=0.95
	else:
		thres=np.mean(diffs[len(diffs)-30:len(diffs)])-3*np.std(diffs[len(diffs)-30:len(diffs)])
	return thres

def train(diff, thres): #identifies if there is a train and saves images for verification if so
	if diff<thres:
		return "TRAIN!"
	else:
		return "no train"

def movefile(trainresult, file1, file2, dest):
	if trainresult=="TRAIN!":
		shutil.copy2(file1, dest)
		shutil.copy2(file2, dest)
	else:
		file1=file1


##Initialize lists and locations for results
diffs=list()
results=list()
dest='/data/train/images/withtrain/'

def train_capture(minutes):
	if minutes==0:
		while True:
			ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
			tslist=ts.split(":")
			minute=int(tslist[1])
			second=int(tslist[2])
			lastmin=lmin(tslist, minute)
			lastsec=lsec(tslist, second)
			tss=tsdelay(tslist, lastmin, lastsec)
			ts1="file-"+tss[0]+"*"
			ts2="file-"+tss[1]+"*"
			ts1files=getfiles(ts1)
			ts2files=getfiles(ts2)
			img1=cv2.imread(ts1files[0])
			img2=cv2.imread(ts2files[0])
			compare=cv2.matchTemplate(img1,img2,cv2.TM_CCORR_NORMED)
			diff=np.amax(compare)
			diffs.append(diff)
			t=thres(diffs)
			result=train(diff, t)
			results.append(result)
			movefile(result, ts1files[0], ts2files[0], dest)
	else:
		timeout=time.time()+60*minutes
		while True:
			if time.time()>timeout:
				break
			ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
			tslist=ts.split(":")
			minute=int(tslist[1])
			second=int(tslist[2])
			lastmin=lmin(tslist, minute)
			lastsec=lsec(tslist, second)
			tss=tsdelay(tslist, lastmin, lastsec)
			ts1="file-"+tss[0]+"*"
			ts2="file-"+tss[1]+"*"
			ts1files=getfiles(ts1)
			ts2files=getfiles(ts2)
			img1=cv2.imread(ts1files[0])
			img2=cv2.imread(ts2files[0])
			compare=cv2.matchTemplate(img1,img2,cv2.TM_CCORR_NORMED)
			diff=np.amax(compare)
			diffs.append(diff)
			t=thres(diffs)
			result=train(diff, t)
			results.append(result)
			movefile(result, ts1files[0], ts2files[0], dest)
