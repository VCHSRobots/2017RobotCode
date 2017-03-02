# ---------------------------------------------------------------------
# camerastream.py -- stream camera output to client
#
# Created Jan 2017 TastyDuck, DLB
# ---------------------------------------------------------------------


from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback
import numpy as np
import evsslogger

logger = evsslogger.getLogger()

class BroadcastStream(threading.Thread):
	def __init__(self, Conn, Addr):
		threading.Thread.__init__(self)
		self.Conn = Conn
		self.Addr = Addr
		self.Cam = None
		self.CamIndex = -1
		self.CamNewIndex = 0
		self.CamSwitchLock = threading.Lock()

	def setCam(self, camindex):
		self.CamSwitchLock.acquire()
		self.CamNewIndex = camindex
		self.CamSwitchLock.release()

	def killCam(self):
		if self.Cam is not None:
			try:
				self.Cam.release()
			except:
				logger.info("Unable to release Cam %d" % self.CamIndex)
		self.Cam = None
		self.CamIndex = -1

	def setCamForReal(self, camindex):
		logger.info("Cam %d Selected" % camindex)
		self.killCam()
		self.CamIndex = camindex
		if self.CamIndex >= 0:
			try:
				self.Cam = cv2.VideoCapture(self.CamIndex)
			except:
				logger.warn("Unable to setup Cam %d for capture" % self.CamIndex)
				self.Cam = None
			if self.CamIndex == 0:
				call(["v4l2-ctl", "-c", "exposure_auto=1"])
				call(["v4l2-ctl", "-c", "exposure_absolute=5"])
				call(["v4l2-ctl", "-c", "brightness=30"])

	def run(self):
		self.setCamForReal(self.CamNewIndex)
		logger.info("BroadcastThread started")
		haveErr = False
		FramesGrabbed = 0
		FPS = 0
		while True:
			err = ""
			StartTime = time.time()
			self.CamSwitchLock.acquire()
			newindex = self.CamNewIndex
			self.CamSwitchLock.release()
			if newindex != self.CamIndex:
				self.setCamForReal(newindex)
			haveFrame = False
			if self.Cam is not None:
				try:
					ret, frame = self.Cam.read()
					haveFrame = True
					haveErr = False
				except:
					if not haveErr:
						logger.error("Unable to take image from Cam %d" % self.CamIndex)
						err = "Cam Error at Jetson"
					haveErr = True
					haveFrame = False
			if not haveFrame:
				frame = np.zeros((480,640,3), np.uint8)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			font = cv2.FONT_HERSHEY_SIMPLEX
			height, width = gray.shape
			CurrentCam = self.CamIndex + 1
			text = "Cam %d @ %dx%d" % (CurrentCam, height, width)
			cv2.putText(gray, text, (10,40), font, 1, (255,255,255), 2, cv2.LINE_AA)
			if err != "":
				cv2.putText(gray, err, (10, 80), font, 1, (255,255,255), 2, cv2.LINE_AA)
			enc = cv2.imencode(".png", gray)[1]
			bin64data = base64.b64encode(enc)
			if self.CamIndex >= 0:
				try:
					self.Conn.sendall(bin64data + "\r\n")
				except:
					logger.error("Unable to send image to client (%s, %s):" % self.Addr)
					logger.error("Shutting down comm port.")
					self.killCam()
					return
			while time.time() - StartTime < 0.1:
				time.sleep(0.01)
