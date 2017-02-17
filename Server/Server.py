#
# VisionSystemServer. Created by: KJF, NG, TastyDucks
#

from __future__ import print_function
from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback
import ds_pi_communication, rio_pi_communication #, field_coordinates

#
#Global variables
#

#Internet

Host = "0.0.0.0"
Port = 5800
RecvBuffer = 1024
ClientBuffer = 16

#Targeting

Hue = [100.0, 125.0]
Saturation = [90.0, 255.0]
Luminance = [20.0, 125.0]
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
	try:
		Message = time.strftime("%Y-%m-%d/%H:%M:%S") + " (" + threading.current_thread().name + ") " + Message
		print(Message)
		with open ("outlog.txt", "a+") as file:
			file.write(Message + "\r\n")
	except:
		print (time.strftime("%Y-%m-%d/%H:%M:%S") + " (" + threading.current_thread().name + ") " + "[EROR] Error with logging system:")
		traceback.print_exc()

class BroadcastStream(threading.Thread):
	def __init__(self, Conn, Addr):
		threading.Thread.__init__(self)
		self.Conn = Conn
		self.Addr = Addr
	def run(self):
		global Cam1
		global Cam2
		global Cam3
		global Cam4
		Log("[INFO] BroadcastThread started.")
		while True:
			while Camera == 0:
				pass
			while Camera == 1:
				try:
					StartTime = time.time()
					try:
						Ret, Frame = Cam1.read()
					except:
						Log("[EROR] Unable to take image from camera 1:")
						traceback.print_exc()
					try:
						Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
					except:
						Log("[EROR] Unable to convert image to grayscale:")
						traceback.print_exc()
					try:
						Enc = cv2.imencode(".png", Gray)[1]
						Bin64Data = base64.b64encode(Enc)
					except:
						Log("[EROR] Unable to convert image to Base 64 data string:")
						traceback.print_exc()
					try:
						Conn.sendall(Bin64Data + "\r\n")
					except:
						Log("[EROR] Unable to send image to client (%s, %s):" %Addr)
						traceback.print_exc()
				except:
					Log("[EROR] Unable to send video stream for camera 1 to client (%s, %s):" %Addr)
					traceback.print_exc()
			while Camera == 2:
				try:
					StartTime = time.time()
					try:
						Ret, Frame = Cam2.read()
					except:
						Log("[EROR] Unable to take image from camera 2:")
						traceback.print_exc()
					try:
						Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
					except:
						Log("[EROR] Unable to convert image to grayscale:")
						traceback.print_exc()
					try:
						Enc = cv2.imencode(".png", Gray)[1]
						Bin64Data = base64.b64encode(Enc)
					except:
						Log("[EROR] Unable to convert image to Base 64 data string:")
						traceback.print_exc()
					try:
						Conn.sendall(Bin64Data + "\r\n")
					except:
						Log("[EROR] Unable to send image to client (%s, %s):" %Addr)
						traceback.print_exc()
				except:
					Log("[EROR] Unable to send video stream for camera 2 to client (%s, %s):" %Addr)
					traceback.print_exc()
			while Camera == 3:
				try:
					StartTime = time.time()
					try:
						Ret, Frame = Cam3.read()
					except:
						Log("[EROR] Unable to take image from camera 3:")
						traceback.print_exc()
					try:
						Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
					except:
						Log("[EROR] Unable to convert image to grayscale:")
						traceback.print_exc()
					try:
						Enc = cv2.imencode(".png", Gray)[1]
						Bin64Data = base64.b64encode(Enc)
					except:
						Log("[EROR] Unable to convert image to Base 64 data string:")
						traceback.print_exc()
					try:
						Conn.sendall(Bin64Data + "\r\n")
					except:
						Log("[EROR] Unable to send image to client (%s, %s):" %Addr)
						traceback.print_exc()
				except:
					Log("[EROR] Unable to send video stream for camera 3 to client (%s, %s):" %Addr)
					traceback.print_exc()
			while Camera == 4:
				try:
					StartTime = time.time()
					try:
						Ret, Frame = Cam4.read()
					except:
						Log("[EROR] Unable to take image from camera 4:")
						traceback.print_exc()
					try:
						Gray = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
					except:
						Log("[EROR] Unable to convert image to grayscale:")
						traceback.print_exc()
					try:
						Enc = cv2.imencode(".png", Gray)[1]
						Bin64Data = base64.b64encode(Enc)
					except:
						Log("[EROR] Unable to convert image to Base 64 data string:")
						traceback.print_exc()
					try:
						Conn.sendall(Bin64Data + "\r\n")
					except:
						Log("[EROR] Unable to send image to client (%s, %s):" %Addr)
						traceback.print_exc()
				except:
					Log("[EROR] Unable to send video stream for camera 4 to client (%s, %s):" %Addr)
					traceback.print_exc()

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
						Log("[INFO] Client (%s, %s) has declared itself as the VisionSystem client." %Addr)
						Stream = BroadcastStream(Conn, Addr)
						Stream.daemon = True
						Stream.name = "BroadcastThread"
						Stream.start()
					elif Data == "C0":
						Camera = 0
						Log("[INFO] Client (%s, %s) has requested that no video stream be broadcasted." %Addr)
					elif Data == "C1":
						Camera = 1
						Log("[INFO] Client (%s, %s) has requested that the video stream for camera 1 be broadcasted." %Addr)
					elif Data == "C2":
						Camera = 2
						Log("[INFO] Client (%s, %s) has requested that the video stream for camera 2 be broadcasted." %Addr)
					elif Data == "C3":
						Camera = 3
						Log("[INFO] Client (%s, %s) has requested that the video stream for camera 3 be broadcasted." %Addr)
					elif Data == "C4":
						Camera = 4
						Log("[INFO] Client (%s, %s) has requested that the video stream for camera 4 be broadcasted." %Addr)
					elif Data == "T":
						Log("[INFO] Client (%s, %s) has requested that targeting start up." %Addr)
						Targeter = TargetingManager(Conn, Addr)
						Targeter.daemon = True
						Targeter.name = "TargetingThread"
						Targeter.start()
					elif Data == "T0":
						Target = 0
						Log("[INFO] Client (%s, %s) has requested that no alignment be made toward any target." %Addr)
					elif Data == "T1":
						Target = 1
						Log("[INFO] Client (%s, %s) has requested that alignment be made toward the high boiler opening." %Addr)
					elif Data == "T2":
						Target = 2
						Log("[INFO] Client (%s, %s) has requested that alignment be made toward the gear delivery peg." %Addr)
					else:
						Log("[EROR] Error parsing data recieved from client (%s, %s): \"" %Addr + Data + "\": valid messages are: \"C\", \"C0\", \"C1\", \"C2\", \"C3\", \"C4\", \"T\", \"T1\", \"T2\".")
				else:
					Log("[INFO] Client (%s, %s) has disconnected." %Addr)
					Camera = 0
					Target = 0
					return
			except:
				Log("[EROR] Error receiving data from client (%s, %s): Client considered disconnected:" %Addr)
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
					if len(BetterContours) == 2:
						for Contour in BetterContours:
							M = cv2.moments(Contour)
							cX = int(M["m10"] / M["m00"])
							cY = int(M["m01"] / M["m00"])
							Centers.append((cX, cY))
						XDistance = abs(Centers[0][0] - Centers[1][0])
						YDistance = abs(Centers[0][1] - Centers[1][1])
						if XDistance < MaxHorizontalOffset and XDistance > MinHorizontalOffset and YDistance < MaxVerticalOffset and YDistance > MinVerticalOffset:
							Height, Width, Channels = Frame.shape
							BetterCenters = [(Centers[0][0], 0), (Centers[1][0], Height)]
							cv2.line(Frame, BetterCenters[0], BetterCenters[1], (255, 255, 255), 1)
				except:
					Log("[EROR] Unable to process image:")
					traceback.print_exc()
				try:
					pass
				except:
					pass
				cv2.imshow("Processed image output:", Frame)
				cv2.waitKey(1)
			while Target == 2:
				pass #WORK IN PROGRESS FOR PEG DELIVERY AUTOAIM TARGETING

#
#Begin mainline code
#

Log("[INFO] VisionSystem Server initiated! | Running on Python version: " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + ". Running on OpenCV version: " + cv2.__version__ + ".")
Camera = 0
Target = 0
ServerManager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(0.1)
ServerManager.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ServerManager.bind((Host, Port))
NumberOfClientThreads = 1

try:
	Log("[INFO] Setting up camera 1...")
	call(["v4l2-ctl", "-c", "exposure_auto=1"])
	call(["v4l2-ctl", "-c", "exposure_absolute=5"])
	call(["v4l2-ctl", "-c", "brightness=30"])
	Cam1 = cv2.VideoCapture(0)
except:
	Log("[EROR] Unable to set up camera 1:")
	traceback.print_exc()
try:
	Log("[INFO] Setting up camera 2...")
	Cam2 = cv2.VideoCapture(1)
except:
	Log("[EROR] Unable to set up camera 2:")
	traceback.print_exc()
try:
	Log("[INFO] Setting up camera 3...")
	Cam3 = cv2.VideoCapture(2)
except:
	Log("[EROR] Unable to set up camera 3:")
	traceback.print_exc()
try:
	Log("[INFO] Setting up camera 4...")
	Cam4 = cv2.VideoCapture(3)
except:
	Log("[EROR] Unable to set up camera 4:")
	traceback.print_exc()

while True:
	ServerManager.listen(ClientBuffer)
	Conn, Addr = ServerManager.accept()
	NewClient = ClientManager(Conn, Addr)
	NewClient.name = "ClientThread:" + str(NumberOfClientThreads)
	NewClient.daemon = True
	NewClient.start()
	NumberOfClientThreads += 1
