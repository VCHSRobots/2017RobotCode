# ---------------------------------------------------------------------
# targetproc.py -- Main targeting processor for Jeston on 2017 EPIC Robot
#
# Created by: TastyDucks, DLB 03/17
# ---------------------------------------------------------------------

# Similar to targeter.py -- but does not use threading.  All calls
# are blocking.

import cv2, socket, time, traceback
from subprocess import call
import numpy as np
import evsslogger
import findtarget

logger = evsslogger.getLogger()

# How to Use this code
# --------------------
#
# To get target "reports", do the following:
# Create a TargetProc object.  A TargetProc object will manage the Cameras
# and hold the state from frame to frame.  Call SetParams() and SetTargetMode()
# on the TargetProc object to set up how you want the target image processed.
# Then for each frame, call Process().  Process will return a "report" which
# is a TargetReport object that holds the info that was obtained by processing
# the camera images.  Note: that the report will always have a valid frame,
# even if the camera are broken.  You may call SetParams and SetTargetMode
# between calls to Process() as often as you like.

class TargetReport:
	def __init__(self, Frame, TargetMode, Valid):
		self.Frame = Frame
		self.TargetMode = TargetMode
		self.Valid = Valid
		self.X1000 = 0
		self.Y1000 = 0
		self.Rect1 = (0, 0, 0, 0)
		self.Rect2 = (0, 0, 0, 0)

	def SetCrossHairs(self, x, y):
		self.X1000 = x
		self.Y1000 = y
	def SetRect1(self, x0, y0, w, h):
		self.Rect1 = (x0, y0, w, h)
	def SetRect2(self, x0, y0, w, h):
		self.Rect2 = (x0, y0, w, h)
	def ToString(self):
		st = "F"
		if self.Valid:
			st = "T"
		tp = (self.TargetMode, st, self.X1000, self.Y1000)
		tp += self.Rect1
		tp += self.Rect2
		return "Mode=%1d, Valid=%s, X,Y=[%4d,%4d] R1=[%3d,%3d,%3d,%3d] R2=[%3d,%3d,%3d,%3d]" % tp
	def ToReport(self):
		#sent at key1=val1;key2=val2;key3=val3...
		i = 0
		if self.Valid:
			i = 1
		tp = (self.TargetMode, i, self.X1000, self.Y1000)
		tp += self.Rect1
		tp += self.Rect2
		return "Mode=%1d;Valid=%1d;X=%d;Y=%d;r0x=%d;r0y=%d;r0w=%d;r0h=%d;r1x=%d;r1y=%d;r1w=%d;r1h=%d" % tp 

class TargetProc:
	def __init__(self):
		self.Cam = None
		self.TargetMode = -1
		self.FrameCount = 0
		self.SwitchCameras = True
		self.Params = Params = findtarget.GetDefaultParams()

	def SwitchCamerasToggle(self):
		self.SwitchCameras = not self.SwitchCameras

	def killTarget(self):
		if self.Cam is not None:
			try:
				self.Cam.release()
			except:
				logger.info("Unable to release Cam %d" % self.TargetIndex)
		self.Cam = None
		self.TargetMode = -1

	def SetParams(self, Params):
		self.Params = Params

	def SetTargetMode(self, targetmode):
		if (targetmode == self.TargetMode) and (self.Cam is not None):
			return
#		if (self.TargetMode == 0):
#			return
		logger.info("Target %d Selected" % targetmode)
		self.killTarget()
		self.TargetMode = targetmode
		if self.TargetMode > 0:
			try:
				CameraIndex = self.TargetMode - 1
				if self.SwitchCameras:
					if CameraIndex == 0:
						CameraIndex = 1
					else:
						CameraIndex = 0
				self.Cam = cv2.VideoCapture(CameraIndex) 
			except:
				logger.warn("Unable to setup Cam %d for capture" % CameraIndex)
				self.Cam = None
			if CameraIndex == 0:
				call(["v4l2-ctl", "-c", "exposure_auto=1"])
				call(["v4l2-ctl", "-c", "exposure_absolute=5"])
				call(["v4l2-ctl", "-c", "brightness=30"])
			elif CameraIndex == 1:
				call(["v4l2-ctl", "--device=1", "-c", "exposure_auto=1"])
				call(["v4l2-ctl", "--device=1", "-c", "exposure_absolute=5"])
				call(["v4l2-ctl", "--device=1", "-c", "brightness=30"])

	def MakeErrorFrame(self, reason):
		Frame = np.zeros((480,640,3), np.uint8)
		cv2.putText(Frame, reason, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
		Ans = TargetReport(Frame, self.TargetMode, False)
		return Ans

	def Process(self):
		if self.TargetMode <= 0:
			return self.MakeErrorFrame("No Target Selected")
		if self.Cam == None:
			return self.MakeErrorFrame("Cam NONE")
		targettype = self.TargetMode - 1
		try:
			ret, Frame = self.Cam.read()
		except Exception as e:
			return self.MakeErrorFrame("Bad Cam Read")
		try:
			Answer = findtarget.FindTarget(Frame, targettype, self.Params)
#			cv2.imshow("TEMP FRAME DISPLAY", Answer[0])
#			cv2.waitKey(1)
		except:
			return self.MakeErrorFrame("Exception From FindTarget")

		if len(Answer)  < 6:
			return self.MakeErrorFrame("Bad N-Tuple from FindTarget")

		Rpt = TargetReport(Answer[0], self.TargetMode, Answer[2])
		Rpt.SetCrossHairs(Answer[3], Answer[4])
		extrastuff = Answer[5]
		if len(extrastuff) != 2:
			logger.warn("Bad N-Tuple from findtarget.")
			return Rpt
		r1 = extrastuff[0]
		r2 = extrastuff[1]
		if len(r1) != 4 or len(r2) != 4:
			logger.warn("Bad N-Tuple from findtarget.")
			return Rpt
		Rpt.SetRect1(r1[0], r1[1], r1[2], r1[3])
		Rpt.SetRect2(r2[0], r2[1], r2[2], r2[3])
		return Rpt

