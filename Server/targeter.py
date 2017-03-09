# ---------------------------------------------------------------------
# targeter.py -- Main targeting system for targeting for Jeston on 2017 EPIC Robot
#
# Created by: TastyDucks, DLB 02/17
# ---------------------------------------------------------------------

import cv2, socket, threading, time, traceback
from subprocess import call
import numpy as np
import evsslogger
import findtarget

logger = evsslogger.getLogger()

#Demonstation variable

Demo = False



class Targeter(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.Cam = None
		self.TargetIndex = -1
		self.TargetNewIndex = 0
		self.TargetSwitchLock = threading.Lock()
		self.AnswerLock = threading.Lock()
		self.Answer = None
		self.FrameCount = 0

	# setTarget(indx) -- Switch targets.
	# 0=none, 1=boiler, 2=peg
	def setTarget(self, targetindex):
		self.TargetSwitchLock.acquire()
		self.TargetNewIndex = targetindex
		self.TargetSwitchLock.release()

	def killTarget(self):
		if self.Cam is not None:
			try:
				self.Cam.release()
			except:
				logger.info("Unable to release Cam %d" % self.TargetIndex)
		self.Cam = None
		self.TargetIndex = -1

	def setTargetForReal(self, targetindex):
		logger.info("Target %d Selected" % targetindex)
		self.killTarget()
		self.TargetIndex = targetindex
		if self.TargetIndex >= 0:
			try:
				self.Cam = cv2.VideoCapture(self.TargetIndex)
			except:
				logger.warn("Unable to setup Cam %d for capture" % self.TargetIndex)
				self.Cam = None
			if self.TargetIndex == 0:
#				call(["v4l2-ctl", "-c", "exposure_auto=1"])
#				call(["v4l2-ctl", "-c", "exposure_absolute=5"])
#				call(["v4l2-ctl", "-c", "brightness=30"])
				pass
			#TODO: Set up exposure for second camera!

	def getAnswer(self):
		self.AnswerLock.acquire()
		Ans = self.Answer
		self.AnswerLock.release()
		if Ans is None:
			Frame = np.zeros((480,640,3), np.uint8)
			Ans = (Frame, -1, False, 0, 0)
#		try:
#			cv2.imshow("Image", Ans[0])
#			cv2.waitKey(10)
#		except:
#			logger.error("Unable to display image!!!")
		return Ans

	#This function finds the target given a camera and a type of target to look for.
	#Type is defined as follows: 0 = High Boiler Target; 1 = Gear Delivery Target.
	#Returns a tuple with the following objects: Image containing the view of the target,
	#An integer detonating the type of targeting used,
	#a boolean flag indicating wheather a target was detected, and the X and Y offset
	#of the target from the center of the image.
	def GetTarget(self, Cam, Type):
		try:
			ret, Frame = Cam.read()
		except Exception as e:
			ret = None
			Frame = None
			logger.error("Unable to take image from cam %d (%s): " % (self.TargetIndex, str(e)))
		if not ret or (Frame is None):
			Frame = np.zeros((480,640,3), np.uint8)
			# ToDo: Write something on the frame to indicate the frame was not from the camera.
			return (Frame, Type, False, 0, 0)
		self.FrameCount += 1
		if self.FrameCount % 250 == 0:
			logger.info("Targeter: %d targeting images processed!" % self.FrameCount)
		Answer = findtarget.FindTarget(Frame, Type)
		DiffFrame = Answer[0]
		Height, Width, Channels = DiffFrame.shape
		cv2.putText(DiffFrame, str(self.FrameCount), (30, Height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
		DiffAnswer = []
		DiffAnswer.append(DiffFrame)
		DiffAnswer.append(Answer[1:])
		return DiffAnswer

	def run(self):
		logger.info("TargetingThread started!")
		while True:
			self.TargetSwitchLock.acquire()
			targetindex = self.TargetNewIndex
			self.TargetSwitchLock.release()
			if targetindex != self.TargetIndex:
				self.setTargetForReal(targetindex)
			try:
				Ans = self.GetTarget(self.Cam, targetindex)
			except Exception as e:
				logger.error("Unable to send offset to client: " + str(e))
				Frame = np.zeros((480,640,3), np.uint8)
				Ans = (Frame, targetindex, False, 0, 0)
			self.AnswerLock.acquire()
			self.Answer = Ans
			self.AnswerLock.release()
