# ---------------------------------------------------------------------
# findtarget.py -- The guts of calculating where the target is.
#
# Created by: TastyDucks, DLB 02/17
# ---------------------------------------------------------------------

import cv2
import numpy as np
import time
import evsslogger
import traceback

logger = evsslogger.getLogger()

#Targeting variables

Hue = [90.0, 125.0]
Saturation = [80.0, 255.0]
Luminance = [10.0, 125.0]
MinArea = 150.0
MinPerimeter = 30.0
MinWidth = 0.0
MaxWidth = 500.0
MinHeight = 10.0
MaxHeight = 1000.0
Solidity = [35.0, 100.0]
MaxVertices = 150.0
MinVertices = 4.0
MinRatio = 1.00
MaxRatio = 4.00
MaxVerticalOffset = 50
MinVerticalOffset = 5
MaxHorizontalOffset = 25
MinHorizontalOffset = 0

PegHue = [90.0, 175.0]
PegSaturation = [90.0, 255.0]
PegLuminance = [25.0, 125.0]
PegMinArea = 500.0
PegMinPerimeter = 0.0
PegMinWidth = 0.0
PegMaxWidth = 1000.0
PegMinHeight = 25.0
PegMaxHeight = 1000.0
PegSolidity = [0.0, 100.0]
PegMaxVertices = 150.0
PegMinVertices = 4.0
PegMinRatio = 0.3
PegMaxRatio = 2.6
PegMaxVerticalOffset = 20
PegMinVerticalOffset = 0
PegMaxHorizontalOffset = 10000
PegMinHorizontalOffset = 0

# FindTarget() -- Given an image (frame) and a type (0=boiler, 1=peg), returns
# the following tuple: (Frame, Type, Flag, px, py, h1, w1, h2, w2), where Frame is the processed
# image with calibration marks, Flag is a bool which indicates if the target was 
# found at all, Type is the type of target being processes, and px,py are offsets 
# from the center of the image. The offsets
# are in 1/1000 of the width or height of the frame.  For
# example 0,0 is the center of the frame, -500,-500 would be the upper left
# corner, and 500,500 would be the lower right corner.
# h1, w1, are the height and with of the first target portion (for GEAR DELIVERY ONLY.)
# h2, w2, are the height and width of the second target portion (for GEAR DELIVERY ONLY.)

def FindTarget(Frame, Type):
	haveErr = False
	#FramesGrabbed = 0
	#FPS = 0
	#BenchmarkTimes = [] #StartGrabTime, StartColorTime, StartEncodeTime, StartSendTime, EndTime
	#AverageTimes = [] #Array containing several copies of BenchmarkTime (s)
	#StartTime = time.time()
	err = ""
	#BenchmarkTimes.append(time.time())
	#self.TargetSwitchLock.acquire()
	#newindex = self.TargetNewIndex
	#self.TargetSwitchLock.release()
	#if newindex != self.TargetIndex:
	#		self.setTargetForReal(newindex)
	haveFrame = False
	try:
		ImHLS = cv2.cvtColor(Frame, cv2.COLOR_BGR2HLS)
		if Type == 0:
			Out = cv2.inRange(ImHLS, (Hue[0], Luminance[0], Saturation[0]), (Hue[1], Luminance[1], Saturation[1]))
			_, OkContours, _ = cv2.findContours(Out, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
			BetterContours = []
			for Contour in OkContours:
				x, y, w, h = cv2.boundingRect(Contour)
				if w > MinWidth and w < MaxWidth:
					if h > MinHeight and h < MaxHeight:
						Area = cv2.contourArea(Contour)
						if Area > MinArea:
							if cv2.arcLength(Contour, True) > MinPerimeter:
								Hull = cv2.convexHull(Contour)
								Solid = 100 * Area / cv2.contourArea(Hull)
								if Solid > Solidity[0] and Solid < Solidity[1]:
									if len(Contour) > MinVertices and len(Contour) < MaxVertices:
										Ratio = (float)(w) / h
										if Ratio > MinRatio and Ratio < MaxRatio:
											BetterContours.append(Contour)
			BetterContours = sorted(BetterContours, key=cv2.contourArea, reverse=True)[:2] #Keep 2 largest
			Centers = []
			Height, Width, Channels = Frame.shape
			cv2.line(Frame, (Width / 2, (Height / 2) - 10), (Width / 2, (Height / 2) + 10), (255, 255, 255), 1) #Crosshair Y
			cv2.line(Frame, ((Width / 2) - 10, Height / 2), ((Width / 2) + 10, Height / 2), (255, 255, 255), 1) #Crosshair X
			if len(BetterContours) == 2:
				for Contour in BetterContours:
					M = cv2.moments(Contour)
					cX = int(M["m10"] / M["m00"])
					cY = int(M["m01"] / M["m00"])
					Centers.append((cX, cY))
				XDistance = abs(Centers[0][0] - Centers[1][0])
				YDistance = abs(Centers[0][1] - Centers[1][1])
				if XDistance < MaxHorizontalOffset and XDistance > MinHorizontalOffset and YDistance < MaxVerticalOffset and YDistance > MinVerticalOffset:
					cv2.line(Frame, (Centers[0][0] + (XDistance / 2), 0), (Centers[0][0] + (XDistance / 2), Height), (255, 255, 255), 1) #Line through center of target Y
					cv2.line(Frame, (0, (Centers[0][1] + Centers[1][1]) / 2), (Width, (Centers[0][1] + Centers[1][1]) / 2), (255, 255, 255), 1) #Line through center of target X
					CenterTarget = (((Centers[0][0] + Centers[1][0]) / 2), (Centers[0][1] + Centers[1][1]) / 2)
					OffsetX = CenterTarget[0] - (Width / 2)
					OffsetY = CenterTarget[1] - (Height / 2)
					Offset1000X = 1000 * (float(OffsetX)/float(Width))
					Offset1000Y = 1000 * (float(OffsetY)/float(Width))
				else:
					# ToDo: write a note in the image on why it failed...
					return Frame, Type, False, 0, 0
			else:
				# ToDo: write a note in the image on why it failed...
				return Frame, Type, False, 0, 0
			Offset = str(Offset1000X) + ", " + str(Offset1000Y)
			cv2.putText(Frame, Offset, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
			return Frame, Type, True, Offset1000X, Offset1000Y
		elif Type == 1:
			Out = cv2.inRange(ImHLS, (PegHue[0], PegLuminance[0], PegSaturation[0]), (PegHue[1], PegLuminance[1], PegSaturation[1]))
			_, OkContours, _ = cv2.findContours(Out, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
			BetterContours = []
			for Contour in OkContours:
				x, y, w, h = cv2.boundingRect(Contour)
				if w > PegMinWidth and w < PegMaxWidth:
					if h > PegMinHeight and h < PegMaxHeight:
						Area = cv2.contourArea(Contour)
						if Area > PegMinArea:		
							if cv2.arcLength(Contour, True) > PegMinPerimeter:
								Hull = cv2.convexHull(Contour)
								Solid = 100 * Area / cv2.contourArea(Hull)
								if Solid > PegSolidity[0] and Solid < PegSolidity[1]:
									if len(Contour) > PegMinVertices and len(Contour) < PegMaxVertices:
										Ratio = (float)(w) / h
										if Ratio > PegMinRatio and Ratio < PegMaxRatio:
											BetterContours.append(Contour)
			Sizes = []
			Centers = []
			Height, Width, Channels = Frame.shape
			cv2.line(Frame, (Width / 2, (Height / 2) - 10), (Width / 2, (Height / 2) + 10), (255, 255, 255), 1) #Crosshair Y
			cv2.line(Frame, ((Width / 2) - 10, Height / 2), ((Width / 2) + 10, Height / 2), (255, 255, 255), 1) #Crosshair X
			if len(BetterContours) >= 2:
				BetterContours = sorted(BetterContours, key=cv2.contourArea, reverse=True)[:2]
				cv2.drawContours(Frame, BetterContours, -1, (0, 200, 0), 2)
				for Contour in BetterContours:
					BoundingX, BoundingY, BoundingWidth, BoundingHeight = cv2.boundingRect(Contour)
					Sizes.append((BoundingWidth, BoundingHeight))
					cv2.putText(Frame, str(BoundingHeight), ((BoundingX + BoundingWidth + 5), (BoundingY + (BoundingHeight / 2))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA) #Height Text
					BoundingTextWidth, BoundingTextHeight = cv2.getTextSize(str(BoundingWidth), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
					cv2.putText(Frame, str(BoundingWidth), ((BoundingX + (BoundingWidth / 2) - BoundingTextWidth), (BoundingY + BoundingHeight + 5 + BoundingTextHeight)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA) #Width Text
					M = cv2.moments(Contour)
					cX = int(M["m10"] / M["m00"])
					cY = int(M["m01"] / M["m00"])
					Centers.append((cX, cY))
				XDistance = abs(Centers[0][0] - Centers[1][0])
				YDistance = abs(Centers[0][1] - Centers[1][1])
				if XDistance < PegMaxHorizontalOffset and XDistance > PegMinHorizontalOffset and YDistance < PegMaxVerticalOffset and YDistance > PegMinVerticalOffset:
					Vector = (Centers[0][0] - Centers[1][0], Centers[0][1] - Centers[1][1])
					Mag = sqrt((Vector[0] * Vector[0]) + )
					cv2.line(Frame, (Centers[0][0] + (XDistance / 2), 0), (Centers[0][0] + (XDistance / 2), Height), (255, 255, 255), 1) #Line through center of target Y
					cv2.line(Frame, (0, Centers[0][1]), (Width, Centers[1][1]), (255, 255, 255), 1) #Line through center of target X
					CenterTarget = (((Centers[0][0] + Centers[1][0]) / 2), (Centers[0][1] + Centers[1][1]) / 2)
					OffsetX = CenterTarget[0] - (Width / 2)
					OffsetY = CenterTarget[1] - (Height / 2)
					Offset1000X = 1000 * (float(OffsetX)/float(Width))
					Offset1000Y = 1000 * (float(OffsetY)/float(Width))
					Offset = str(Offset1000X) + ", " + str(Offset1000Y)
				else:
					Offset = "?, ?"
					cv2.putText(Frame, Offset, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
					return Frame, Type, False, 0, 0, 0, 0, 0, 0
			else:
				Offset = "?, ?"
				cv2.putText(Frame, Offset, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
				return Frame, Type, False, 0, 0, 0, 0, 0, 0
			cv2.putText(Frame, Offset, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
			return Frame, Type, True, Offset1000X, Offset1000Y, Sizes[0][0], Sizes[0][1], Sizes[1][0], Sizes[1][1]
	except Exception as e:
		logger.error("Error autoaiming! " + str(e))
		traceback.print_exc()
		#ToDo: write something in the frame to say what the exception was.
		return (Frame, Type, False, 0, 0)
