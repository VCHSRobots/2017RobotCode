# ---------------------------------------------------------------------
# camerastream.py -- stream camera output to client
#
# Created Jan 2017 TastyDuck, DLB
# ---------------------------------------------------------------------


from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback
import evsslogger

logger = evsslogger.getLogger()

class BroadcastStream(threading.Thread):
	def __init__(self, Conn, Addr):
		threading.Thread.__init__(self)
		self.Conn = Conn
		self.Addr = Addr
		self.Cam = None
		self.CamIndex = -1
		self.CamNewIndex = -1
		self.CamSwitchLock = threading.Lock()

	def setCam(self, camindex):
		self.CamSwitchLock.acquire()
		self.CamNewIndex = camindex
		self.CamSwitchLock.release()

	def setCamForReal(self, camindex):
		logger.info("Cam %d Selected" % camindex) 
		if self.Cam is not None:
			try: 
				self.Cam.release()
			except:
				logger.info("Unable to release Cam %d" % self.CamIndex)
		self.Cam = None
		self.CamIndex = camindex
		if self.CamIndex >= 0:
			try:
				#call(["v4l2-ctl", "-c", "exposure_auto=1"])
				#call(["v4l2-ctl", "-c", "exposure_absolute=5"])
				#call(["v4l2-ctl", "-c", "brightness=30"])qqqqqqqqwdwadsadswsswssadwwwswswsaa
				self.Cam = cv2.VideoCapture(self.CamIndex)
			except:
				logger.warn("Unable to setup Cam %d for capture" % self.CamIndex)
				self.Cam = None

	def run(self):
		logger.info("BroadcastThread started.")
		haveErr = False
		while True:			
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
					haveFrame = true
					haveErr = False				
				except:
					if not haveErr:
						logger.error("Unable to take image from Cam %d" % self.CamIndex)
					haveErr = True
					#traceback.print_exc()
			else:
				logger.warn("Camera is none.")
			if haveFrame:
				try:
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
				except:
					logger.error("Unable to convert image to grayscale:")
					#traceback.print_exc()
				try:
					enc = cv2.imencode(".png", gray)[1]
					bin64data = base64.b64encode(enc)
				except:
					logger.error("Unable to convert image to Base 64 data string:")
					#traceback.print_exc()
				try:
					logger.info("sending data (%d)" % len(bin64data))
					self.Conn.sendall(bin64data + "\r\n")
				except:
					logger.error("Unable to send image to client (%s, %s):" % self.Addr)
					#traceback.print_exc()
			while time.time() - StartTime < 0.1:
				time.sleep(0.01)




