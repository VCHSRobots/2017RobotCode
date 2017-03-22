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
		self.Rect1 = (0, 0)
		self.Rect2 = (0, 0)
	def SetCrossHairs(self, x, y):
		self.X1000 = x
		self.Y1000 = y
	def SetRect1(self, x, y):
		self.Rect1 = (x, y)
	def SetRect2(self, x, y):
		self.Rect2 = (x, y)
	def ToString(self):
		st = "F"
		if self.Valid:
			st = "T"
		tp = (self.TargetMode, st, self.X1000, self.Y1000)
		tp += self.Rect1
		tp += self.Rect2
		return "Mode=%1d, Valid=%s, X,Y=[%4d,%4d] Rects=[%3d,%3d,%3d,%3d]" % tp

class TargetProc:
	def __init__(self):
		self.Cam = None
		self.TargetMode = -1
		self.FrameCount = 0
		self.Params = Params = findtarget.GetDefaultParams()

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
		logger.info("Target %d Selected" % targetmode)
		self.killTarget()
		self.TargetMode = targetmode
		if self.TargetMode > 0:
			try:
				CameraIndex = self.TargetMode - 1
				self.Cam = cv2.VideoCapture(CameraIndex) 
			except:
				logger.warn("Unable to setup Cam %d for capture" % CameraIndex)
				self.Cam = None
			if self.TargetMode == 1:
				call(["v4l2-ctl", "-c", "exposure_auto=1"])
				call(["v4l2-ctl", "-c", "exposure_absolute=5"])
				call(["v4l2-ctl", "-c", "brightness=30"])
			elif self.TargetMode == 2:
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
		Rpt = TargetReport(Answer[0], self.TargetMode, Answer[2])
		Rpt.SetCrossHairs(Answer[3], Answer[4])
		Rpt.SetRect1(Answer[5], Answer[6])
		Rpt.SetRect2(Answer[7], Answer[8])
		return Rpt

