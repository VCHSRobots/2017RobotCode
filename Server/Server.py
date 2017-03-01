#
# VisionSystemServer. Created by: KJF, NG, TastyDucks
#

from __future__ import print_function
from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback
import ds_pi_communication, rio_pi_communication #, field_coordinates
import evsslogger
import camerastream

#
#Global variables
#

# Logging
logger = evsslogger.getLogger()

#Internet

Host = "0.0.0.0"
Port = 5800
RecvBuffer = 1024
ClientBuffer = 16

#Targeting

Hue = [90.0, 125.0]
Saturation = [80.0, 255.0]
Luminance = [10.0, 125.0]
MinArea = 150.0
MinPerimeter = 30.0
MinWidth = 0.0
MaxWidth = 500.0
MinHeight = 10.0
MaxHeight = 1000.0
Solidity = [35.07194244604317, 100.0]
MaxVertices = 150.0
MinVertices = 4.0
MinRatio = 1.00
MaxRatio = 4.00
MaxVerticalOffset = 50
MinVerticalOffset = 5
MaxHorizontalOffset = 25
MinHorizontalOffset = 0

#
#Functions, classes, et cetera
#

def Log(Message):
	logger.info(Message)

class ClientManager(threading.Thread):
	def __init__(self, Conn, Addr):
		threading.Thread.__init__(self)
		self.Conn = Conn
		self.Addr = Addr
	def run(self):
		global Camera
		global Target
		Log("[INFO] Client (%s, %s) connected and situated." %Addr)
		while True:
			try:
				Data = Conn.recv(RecvBuffer)
				if Data:
					Data = Data.rstrip()
					if Data == ("Requesting ds_pi_communication"):
						ds_pi_communication.run(Conn, Addr)
					elif Data == ("Requesting rio_pi_communication"):
						Conn.settimeout(1)
						rio_pi_communication.run(Conn, Addr)
					elif Data == ("Requesting field_coordinates"):
						field_coordinates.run(Conn, Addr)
					elif Data == "C":
						logger.info("Client (%s, %s) has declared itself as the VisionSystem client." %Addr)
						self.Stream = camerastream.BroadcastStream(Conn, Addr)
						self.Stream.daemon = True
						self.Stream.name = "BroadcastThread"
						self.Stream.start()            
					elif Data == "C0":
						if self.Stream is None:
							logger.warn("Client (%s, %s) video request out of order." % Addr)
							continue
						self.Stream.setCam(-1)
						Camera = 0
						logger.info("Client (%s, %s) has requested that no video stream be broadcasted." %Addr)
					elif Data == "C1" or Data == "C2" or Data == "C3" or Data == "C4":
						if self.Stream is None:
							logger.warn("Client (%s, %s) video request out of order." % Addr)
							continue
						indx = ord(Data[1:2]) - ord('0')
						if indx <= 0 or indx > 4:
							logger.error("Programming ERROR!")
							sys.exit() 
						self.Stream.setCam(indx - 1)
						Camera = indx
						logger.info("Client (%s, %s)" % Addr + " has requested that the video stream for camera %d be broadcasted." % Camera)
					elif Data == "T":
						logger.info("Client (%s, %s) has requested that targeting start up." % Addr)
						Targeter = TargetingManager(Conn, Addr)
						Targeter.daemon = True
						Targeter.name = "TargetingThread"
						Targeter.start()
					elif Data == "T0":
						Target = 0
						logger.info("Client (%s, %s) has requested that no alignment be made toward any target." %Addr)
					elif Data == "T1":
						Target = 1
						logger.info("Client (%s, %s) has requested that alignment be made toward the high boiler opening." %Addr)
					elif Data == "T2":
						Target = 2
						logger.info("Client (%s, %s) has requested that alignment be made toward the gear delivery peg." %Addr)
					else:
						logger.error("Error parsing data recieved from client (%s, %s): \"" %Addr + Data + "\": valid messages are: \"C\", \"C0\", \"C1\", \"C2\", \"C3\", \"C4\", \"T\", \"T1\", \"T2\".")
				else:
					logger.info("Client (%s, %s) has disconnected." %Addr)
					Camera = 0
					Target = 0
					return
			except:
				logger.error("Error receiving data from client (%s, %s): Client considered disconnected:" %Addr)
				traceback.print_exc()
				Conn.close()
				Camera = 0
				Target = 0
				return

class TargetingManager(threading.Thread):
	def __init__(self, Conn, Addr):
		threading.Thread.__init__(self)
		self.Conn = Conn
		self.Addr = Addr
	def run(self):
		global Target
		global Cam1
		global Cam2
		global Cam3
		global Cam4
		global Hue
		global Saturation
		global Luminance
		global MinArea
		global MinPerimeter
		global MinWidth
		global MaxWidth
		global MinHeight
		global MaxHeight
		global Solidity
		global MaxVertices
		global MinVertices
		global MinRatio
		global MaxRatio
		global MaxVerticalOffset
		global MinVerticalOffset
		global MaxHorizontalOffset
		global MinHorizontalOffset
		Log("[INFO] TargetingManager thread started.")
		while True:
			while Target == 0:
				pass
			while Target == 1:
				StartTime = time.time()
				try:
					Ret, Frame = Cam1.read()
				except:
					Log("[EROR] Unable to take image from camera 1 (shooter):")
					traceback.print_exc()
				try:
					ImHLS = cv2.cvtColor(Frame, cv2.COLOR_BGR2HLS)
					Out = cv2.inRange(ImHLS, (Hue[0], Luminance[0], Saturation[0]), (Hue[1], Luminance[1], Saturation[1]))
					OkContours, Hierarchy = cv2.findContours(Out, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
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
					cv2.drawContours(Frame, BetterContours, -1, (0, 200, 0), 2)
					Centers = []
					Height, Width, Channels = Frame.shape
					cv2.line(Frame, (Width / 2, (Height / 2) - 10), (Width / 2, (Height / 2) + 10), (255, 255, 255), 1) #Crosshair Y
					cv2.line(Frame, ((Width / 2) - 10, Height / 2), ((Width / 2) + 10, Height / 2), (255, 255, 255), 1) #Crosshair X
					CenterImage = ((Width / 2, Height / 2))
					if len(BetterContours) == 2:
						for Contour in BetterContours:
							M = cv2.moments(Contour)
							cX = int(M["m10"] / M["m00"])
							cY = int(M["m01"] / M["m00"])
							Centers.append((cX, cY))
						XDistance = abs(Centers[0][0] - Centers[1][0])
						YDistance = abs(Centers[0][1] - Centers[1][1])
						if XDistance < MaxHorizontalOffset and XDistance > MinHorizontalOffset and YDistance < MaxVerticalOffset and YDistance > MinVerticalOffset:
							LinePoints = [(Centers[0][0], 0), (Centers[1][0], Height)]
							cv2.line(Frame, (Centers[0][0], 0), (Centers[1][0], Height), (255, 255, 255), 1) #Line through center of target Y
							cv2.line(Frame, (0, (Centers[0][1] + Centers[1][1]) / 2), (Width, (Centers[0][1] + Centers[1][1]) / 2), (255, 255, 255), 1) #Line through center of target X
							CenterTarget = (((Centers[0][0] + Centers[1][0]) / 2), (Centers[0][1] + Centers[1][1]) / 2)
							cv2.line(Frame, CenterTarget, ((Width / 2), (Height / 2)), (255, 255, 255), 1) #Line connecting center of target and center of image
							OffsetX = CenterTarget[0] - (Width / 2)
							OffsetY = CenterTarget[1] - (Height / 2)
							Offset = "<" + str(OffsetX) + "," + str(OffsetY) + ">"
						else:
							Offset = "<?,?>"
					else:
						Offset = "<?,?>"
				except:
					Log("[EROR] Unable to process image:")
					traceback.print_exc()
				cv2.putText(Frame, Offset, 30, 30, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
				cv2.imshow("Processed image output:", Frame)
				cv2.waitKey(1)
			while Target == 2:
				pass #WORK IN PROGRESS FOR PEG DELIVERY AUTOAIM TARGETING



#
#Begin mainline code
#
evsslogger.initLogging()
Camera = 0
Target = 0
ServerManager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(0.1)
ServerManager.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ServerManager.bind((Host, Port))
NumberOfClientThreads = 1
logger.info("Starting Camera Stream.")

logger.info("Starting Listen loop")

while True:
	ServerManager.listen(ClientBuffer)
	Conn, Addr = ServerManager.accept()
	NewClient = ClientManager(Conn, Addr)
	NewClient.name = "ClientThread:" + str(NumberOfClientThreads)
	NewClient.daemon = True
	NewClient.start()
        logger.info("Client Added")
	NumberOfClientThreads += 1
