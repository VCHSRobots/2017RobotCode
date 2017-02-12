#
# VisionSystemServer. Created by: KJF, NG, TastyDucks
#

from __future__ import print_function
import base64, cv2, socket, sys, threading, time, traceback
import ds_pi_communication, rio_pi_communication #, field_coordinates

#
#Global variables
#

Host = "0.0.0.0"
Port = 5800
RecvBuffer = 1024
ClientBuffer = 16

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
		Log("[INFO] BroadcastStream thread started.")
		try:
			Log("[INFO] Setting up camera 1...")
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
					else:
						Log("[EROR] Error parsing data recieved from client (%s, %s): \"" %Addr + Data + "\": valid messages are: \"C0\", \"C1\", \"C2\", \"C3\", \"C4\".")
				else:
					Log("[INFO] Client (%s, %s) has disconnected." %Addr)
					return
			except:
				Log("[EROR] Error receiving data from client (%s, %s): Client considered disconnected:" %Addr)
				traceback.print_exc()
				Conn.close()
				return

#
#Begin mainline code
#

Log("[INFO] VisionSystem Server initiated! | Running on Python version: " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + ". Running on OpenCV version: " + cv2.__version__ + ".")
Camera = 0
ServerManager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(0.1)
ServerManager.bind((Host, Port))
NumberOfClientThreads = 1
while True:
	ServerManager.listen(ClientBuffer)
	Conn, Addr = ServerManager.accept()
	NewClient = ClientManager(Conn, Addr)
	NewClient.name = "ClientThread:" + str(NumberOfClientThreads)
	NewClient.daemon = True
	NewClient.start()
	NumberOfClientThreads += 1
