# ---------------------------------------------------------------------
# findtargetsimple.py -- The guts of calculating where the target is - but with a lot less filtering!
#
# Created by: TastyDucks, DLB 02/17
# ---------------------------------------------------------------------

import cv2
import numpy as np
import time
import evsslogger
import traceback
import math

logger = evsslogger.getLogger()

def GetDefaultParams():
	p = {}
	p["HueLow"] = 90.0
	p["HueHigh"] = 125.0
	p["SaturationLow"] = 80.0
	p["SaturationHigh"] = 255.0
	p["LuminanceLow"] = 10.0
	p["LuminanceHigh"] = 125.0
	p["MinArea"] = 150.0
	p["MinPerimeter"] = 30.0
	p["MinWidth"] = 0.0
	p["MaxWidth"] = 500.0
	p["MinHeight"] = 10.0
	p["MaxHeight"] = 1000.0
	p["SolidityLow"] = 35.0
	p["SolidityHigh"] = 100.0
	p["MaxVertices"] = 150.0
	p["MinVertices"] = 4.0
	p["MinRatio"] = 1.00
	p["MaxRatio"] = 4.00
	p["MaxVerticalOffset"] = 2000.0
	p["MinVerticalOffset"] = 0.0
	p["MaxHorizontalOffset"] = 10000.0
	p["MinHorizontalOffset"] = 0.0
	p["PegHueLow"] = 90.0
	p["PegHueHigh"] = 175.0
	p["PegSaturationLow"] = 90.0
	p["PegSaturationHigh"] = 255.0
	p["PegLuminanceLow"] = 25.0
	p["PegLuminanceHigh"] = 125.0
	p["PegMinArea"] = 500.0
	p["PegMinPerimeter"] = 0.0
	p["PegMinWidth"] = 0.0
	p["PegMaxWidth"] = 1000.0
	p["PegMinHeight"] = 25.0
	p["PegMaxHeight"] = 1000.0
	p["PegSolidityLow"] = 0.0
	p["PegSolidityHigh"] = 100.0
	p["PegMaxVertices"] = 150.0
	p["PegMinVertices"] = 4.0
	p["PegMinRatio"] = 0.3
	p["PegMaxRatio"] = 2.6
	p["PegMaxVerticalOffset"] = 2000.0
	p["PegMinVerticalOffset"] = 0.0
	p["PegMaxHorizontalOffset"] = 10000.0
	p["PegMinHorizontalOffset"] = 0.0
	return p

Extra = 0

CurrentParams = GetDefaultParams()

def pp(name, default):
	global CurrentParams
	if name in CurrentParams:
		return CurrentParams[name]
	else:
		return default

def DrawData(Frame, Height, Width, Mode, Offset, Distance, FPS, FrameCount):

	global Extra
	#Draw the crosshair.
        cv2.line(Frame, (Width / 2, Height / 2 - 10), (Width / 2, Height / 2 + 10), (255, 255, 255), 1)
        cv2.line(Frame, (Width / 2 - 10, Height / 2), (Width / 2 + 10, Height / 2), (255, 255, 255), 1)

        #Draw image half-way markers.
        cv2.line(Frame, (Width / 2, 0), (Width / 2, 10), (255, 255, 255), 1)
        cv2.line(Frame, (Width / 2, Height), (Width / 2, Height -10), (255, 255, 255), 1)
        cv2.line(Frame, (0, Height / 2), (10, Height / 2), (255, 255, 255), 1)
        cv2.line(Frame, (Width, Height / 2), (Width - 10, Height / 2), (255, 255, 255), 1)

	#Draw image information on the screen.
        Font = cv2.FONT_HERSHEY_SIMPLEX
        Color = (44, 44, 44)
        ModeString = "Mode: " + Mode
        OffsetString = "Offset: " + Offset
        DistanceString = "Est. Distance: " + str(Distance)
        FPSString = "FPS: " + FPS
        FrameCountString = "Frames: " + str(FrameCount)
	ExtraString = "Extra: " + str(Extra)
        WA, HA = cv2.getTextSize(ModeString, Font, 0.5, 1)[0]
        WB, HB = cv2.getTextSize(OffsetString, Font, 0.5, 1)[0]
        WC, HC = cv2.getTextSize(DistanceString, Font, 0.5, 1)[0]
        WD, HD = cv2.getTextSize(FPSString, Font, 0.5, 1)[0]
        WE, HE = cv2.getTextSize(FrameCountString, Font, 0.5, 1)[0]
	WF, HF = cv2.getTextSize(ExtraString,      Font, 0.5, 1)[0]
        HA += 15
        HB += 5
        HC += 5
        HD += 5
        HE += 5
	HF += 5
	cv2.rectangle(Frame, (5, 5), (max(WA, WB, WC, WD, WE, WF) + 15, HA + HB + HC + HD + HE + HF), (44, 44, 44), -1)
        cv2.rectangle(Frame, (10, 10), (max(WA, WB, WC, WD, WE, WF) + 20, HA + HB + HC + HD + HE + HF + 5), (160, 160, 160), -1)
        cv2.putText(Frame, ModeString, (15, HA), Font, 0.5, Color, 1, cv2.LINE_AA)
        cv2.putText(Frame, OffsetString,     (15, HA + HB), Font, 0.5, Color, 1, cv2.LINE_AA)
        cv2.putText(Frame, DistanceString,   (15, HA + HB + HC), Font, 0.5, Color, 1, cv2.LINE_AA)
        cv2.putText(Frame, FPSString,        (15, HA + HB + HC + HD), Font, 0.5, Color, 1, cv2.LINE_AA)
        cv2.putText(Frame, FrameCountString, (15, HA + HB + HC + HD + HE), Font, 0.5, Color, 1, cv2.LINE_AA)
	cv2.putText(Frame, ExtraString,      (15, HA + HB + HC + HD + HE + HF), Font, 0.5, Color, 1, cv2.LINE_AA)
	return Frame

# FindTarget() -- Given an image (frame) and a type (0=boiler, 1=peg), returns
# the following tuple: (Frame, Type, Flag, px, py, h1, w1, h2, w2), where Frame is the processed
# image with calibration marks, Flag is a bool which indicates if the target was 
# found at all, Type is the type of target being processes, and px,py are offsets 
# from the center of the image. The offsets
# are in 1/1000 of the width or height of the frame.  For
# example 0,0 is the center of the frame, -500,-500 would be the upper left
# corner, and 500,500 would be the lower right corner.
# h1, w1, are the height and width of the first target portion, while
# h2, w2, are the height and width of the second target portion.

FrameCount = 0

def FindTarget(Frame, Type, params):
	global FrameCount
	global CurrentParams
	#global Extra
	CurrentParams = params
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
		FrameCount += 1
		ImHLS = cv2.cvtColor(Frame, cv2.COLOR_BGR2HLS)
		if Type == 0:
			StartTime = time.time()
			Out = cv2.inRange(ImHLS, (pp("HueLow", 90.0), pp("LuminanceLow", 10.0), pp("SaturationLow", 255.0)), (pp("HueHigh", 125.0), pp("LuminanceHigh", 125.0), pp("SaturationHigh", 255.0)))
			_, OkContours, _ = cv2.findContours(Out, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
			BetterContours = OkContours
			Sizes = []
			Centers = []
			Height, Width, Channels = Frame.shape
			Extra = len(BetterContours)
			if len(BetterContours) >= 2:
				BetterContours = sorted(BetterContours, key=cv2.contourArea, reverse=True)[:2] #Keep 2 largest
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
				if XDistance < pp("MaxHorizontalOffset", 25) and XDistance >= pp("MinHorizontalOffset", 0) and YDistance < pp("MaxVerticalOffset", 50) and YDistance >= pp("MinVerticalOffset", 5):
					VectorX = Centers[1][0] - Centers[0][0]
					VectorY = Centers[1][1] - Centers[0][1]
					Mag = math.sqrt(VectorX * VectorX + VectorY * VectorY)
					if int(Mag) != 0:
						VectorX = VectorX / Mag
						VectorY = VectorY / Mag
					else:
						Mag = 1
					Distance = Height + Width
					MidpointX = (Centers[0][0] + Centers[1][0]) / 2
					MidpointY = (Centers[0][1] + Centers[1][1]) / 2
					cv2.circle(Frame, (MidpointX, MidpointY), 8, (0, 200, 0), -1) #Circle on midpoint
					RegLineStart = (int(MidpointX + VectorX * Distance), int(MidpointY + VectorY * Distance))
					RegLineEnd = (int(MidpointX + VectorX * -Distance), int(MidpointY + VectorY * -Distance))
					Temp = VectorX
					VectorX = -VectorY
					VectorY = Temp
					PerpLineStart = (int(MidpointX + VectorX * Distance), int(MidpointY + VectorY * Distance))
					PerpLineEnd = (int(MidpointX + VectorX * -Distance), int(MidpointY + VectorY * -Distance))
					cv2.line(Frame, RegLineStart, RegLineEnd, (255, 255, 255), 1) #Line through center of target Y
					cv2.line(Frame, PerpLineStart, PerpLineEnd, (255, 255, 255), 1) #Line through center of target X
					CenterTarget = (MidpointX, MidpointY)
					OffsetX = CenterTarget[0] - (Width / 2)
					OffsetY = CenterTarget[1] - (Height / 2)
					Offset1000X = 1000 * (float(OffsetX)/float(Width))
					Offset1000Y = 1000 * (float(OffsetY)/float(Width))
				else:
					# ToDo: write a note in the image on why it failed...
       					#Calculate average FPS.
				       	FPS = str(int(round(1 / (time.time() - StartTime))))
					Frame = DrawData(Frame, Height, Width, "BOILER", "?, ?", "?", FPS, FrameCount)
					return Frame, Type, False, 0, 0, 0, 0, 0, 0
			else:
				# ToDo: write a note in the image on why it failed...
       				#Calculate average FPS.
				FPS = str(int(round(1 / (time.time() - StartTime))))
				Frame = DrawData(Frame, Height, Width, "BOILER", "?, ?", "?", FPS, FrameCount)
				return Frame, Type, False, 0, 0, 0, 0, 0, 0

			Offset = str(Offset1000X) + ", " + str(Offset1000Y)
       			#Calculate average FPS.
			FPS = str(int(round(1 / (time.time() - StartTime))))
			#Calculate distance.
			Distance = 10 #TEMPORARY!
			Frame = DrawData(Frame, Height, Width, "BOILER", Offset, Distance, FPS, FrameCount)
			return Frame, Type, True, Offset1000X, Offset1000Y

		elif Type == 1:
			StartTime = time.time()
			Out = cv2.inRange(ImHLS, (pp("PegHueLow", 90.0), pp("PegLuminanceLow", 25.0), pp("PegSaturationLow", 90.0)), (pp("PegHueHigh", 175.0), pp("PegLuminanceHigh", 125.0), pp("PegSaturationHigh", 255.0)))
			_, OkContours, _ = cv2.findContours(Out, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
			BetterContours = OkContours
			Sizes = []
			Centers = []
			Height, Width, Channels = Frame.shape
			if len(BetterContours) >= 2:
				BetterContours = sorted(BetterContours, key=cv2.contourArea, reverse=True)[:2] #Keep 2 largest
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
				if XDistance < pp("PegMaxHorizontalOffset", 10000) and XDistance > pp("PegMinHorizontalOffset", 0) and YDistance < pp("PegMaxVerticalOffset", 2000) and YDistance > pp("PegMinVerticalOffset", 0):
					VectorX = Centers[1][0] - Centers[0][0]
					VectorY = Centers[1][1] - Centers[0][1]
					Mag = math.sqrt(VectorX * VectorX + VectorY * VectorY)
					if int(Mag) != 0:
						VectorX = VectorX / Mag
						VectorY = VectorY / Mag
					else:
						Mag = 1
					Distance = Height + Width
					MidpointX = (Centers[0][0] + Centers[1][0]) / 2
					MidpointY = (Centers[0][1] + Centers[1][1]) / 2
					cv2.circle(Frame, (MidpointX, MidpointY), 8, (0, 200, 0), -1) #Circle on midpoint
					RegLineStart = (int(MidpointX + VectorX * Distance), int(MidpointY + VectorY * Distance))
					RegLineEnd = (int(MidpointX + VectorX * -Distance), int(MidpointY + VectorY * -Distance))
					Temp = VectorX
					VectorX = -VectorY
					VectorY = Temp
					PerpLineStart = (int(MidpointX + VectorX * Distance), int(MidpointY + VectorY * Distance))
					PerpLineEnd = (int(MidpointX + VectorX * -Distance), int(MidpointY + VectorY * -Distance))
					cv2.line(Frame, RegLineStart, RegLineEnd, (255, 255, 255), 1) #Line through center of target Y
					cv2.line(Frame, PerpLineStart, PerpLineEnd, (255, 255, 255), 1) #Line through center of target X
					CenterTarget = (MidpointX, MidpointY)
					OffsetX = CenterTarget[0] - (Width / 2)
					OffsetY = CenterTarget[1] - (Height / 2)
					Offset1000X = 1000 * (float(OffsetX)/float(Width))
					Offset1000Y = 1000 * (float(OffsetY)/float(Width))
				else:
	       				#Calculate average FPS.
					FPS = str(int(round(1 / (time.time() - StartTime))))
					Frame = DrawData(Frame, Height, Width, "GEAR", "?, ?", "?", FPS, FrameCount)
					return Frame, Type, False, 0, 0, 0, 0, 0, 0
			else:
	       			#Calculate average FPS.
				FPS = str(int(round(1 / (time.time() - StartTime))))
				Frame = DrawData(Frame, Height, Width, "GEAR", "?, ?", "?", FPS, FrameCount)
				return Frame, Type, False, 0, 0, 0, 0, 0, 0
			Offset = str(Offset1000X) + ", " + str(Offset1000Y)
       			#Calculate average FPS.
			FPS = str(int(round(1 / (time.time() - StartTime))))
			#Calculate distance.
			Distance = 10 #TEMPORARY!
			Frame = DrawData(Frame, Height, Width, "GEAR", Offset, Distance, FPS, FrameCount)
			return Frame, Type, True, Offset1000X, Offset1000Y, Sizes[0][0], Sizes[0][1], Sizes[1][0], Sizes[1][1]
	except Exception as e:
		logger.error("Error autoaiming! " + str(e))
		traceback.print_exc()
		#ToDo: write something in the frame to say what the exception was.
		return (Frame, Type, False, 0, 0)
