# ---------------------------------------------------------------------
# allcams.py -- Test ability to all cameras
#
# Created 03/01/17 DLB
# ---------------------------------------------------------------------

import cv2
import numpy as np

blank_image = np.zeros((480,640,3), np.uint8)
blank_image2 = np.zeros((480,640,3), np.uint8)

def getBlankImage():
	global blank_image, blank_image2
	np.copyto(blank_image, blank_image2)
	return blank_image

def findCams():
	cams = []
	for indx in range(4):
		try:
			cam = cv2.VideoCapture(indx) 
		except:
			cam = None 
		cams.append(cam)
	return cams

def prepareImg(indx, cam):
	err = ""	
	if cam is None:
		img = getBlankImage() 
		err = "No Cam"
	else:
		ret_val, img = cam.read()
		if not ret_val:
			img = getBlankImage() 
			err = "Bad Read"
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(img, "Cam %d" % indx, (10,40), font, 1, (255,255,255), 2, cv2.LINE_AA)
	if err != "":
		cv2.putText(img, err, (10, 80), font, 1, (255,255,255), 2, cv2.LINE_AA)
	img = cv2.resize(img, (320,240))
	return img

def prepareFrame(cams):
	frame = np.zeros((480,640,3), np.uint8)
	parts = [(0,0,0),(240,0,1),(0,320,2),(240,320,3)]
	for p in parts:
		iy,ix,indx = p
		subimg = prepareImg(indx, cams[indx])
		frame[iy:iy+240,ix:ix+320] = subimg
	return frame

def showCams(mirror=False):
	Cams = findCams()
	while True:
		img = prepareFrame(Cams) 
		cv2.imshow('All WebCams', img)
		key = cv2.waitKey(1)
		if key == 27:
			break 

if __name__ == '__main__':
	showCams()



