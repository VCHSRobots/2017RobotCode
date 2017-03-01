# ---------------------------------------------------------------------
# testcams.py -- Test ability to see cameras
#
# Created 02/28/17 DLB
# ---------------------------------------------------------------------

import cv2
import numpy as np

blank_image = np.zeros((480,640,3), np.uint8)
blank_image2 = np.zeros((480,640,3), np.uint8)

def getBlankImage():
	global blank_image, blank_image2
	np.copyto(blank_image, blank_image2)
	return blank_image

def show_webcam(mirror=False):
	indx = -1
	cam = None
	while True:
		indx += 1
		if indx > 5:
			indx = 0 
		err = ""
		if cam is not None:
			try:
				cam.release() 
			except:
				print("Error: unable to release cam %d." % indx)
			cam = None
		try:
			print("Capturing Cam %d" % indx)
			cam = cv2.VideoCapture(indx)
		except:
			#print("Error: Unable to capture cam %d" % indx)
			err = "Unable to Capture"
			cam = None
		while True:
			if cam is not None:
				ret_val, img = cam.read()
				if not ret_val:
					img = getBlankImage()
					err = "Read malfunction"
				else:
					err = ""
				if mirror: 
					img = cv2.flip(img, 1)
			else:
				img = getBlankImage()
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(img, "Cam %d" % indx, (10,40), font, 1, (255,255,255), 2, cv2.LINE_AA)
			cv2.putText(img, "Space Bar for next Cam", (10, 80), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
			if err != "":
				cv2.putText(img, err, (10, 120), font, 1, (255,255,255), 2, cv2.LINE_AA)
			cv2.putText(img, "%dx%d" % img.shape[0:2], (10,160), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
			cv2.imshow('Test WebCam', img)
			key = cv2.waitKey(1)
			if key >= ord('0') and key <= ord('5'):
				indx = key - ord('0') - 1 
				break
			if key == 27 or key == 32:  #esc to quit, space to go to next camera
				break
		if key == 27:
			break

	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=False)

if __name__ == '__main__':
	main()
	
