#
# VisionSystemServer. Created by: KJF, NG, TastyDucks
#

from __future__ import print_function
from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback
import ds_pi_communication, rio_pi_communication #, field_coordinates
import evsslogger
import camerastream
import targetingmanager

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
		self.Stream = None
		self.Targeter = None

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
					elif Data == "C" or Data == "C0" or Data == "C1" or Data == "C2" or Data == "C3" or Data == "C4":
						if self.Stream is None:
							logger.info("Client (%s, %s) has declared itself as the VisionSystem client." %Addr)
							self.Stream = camerastream.BroadcastStream(self.Conn, self.Addr)
							self.Stream.daemon = True
							self.Stream.name = "BroadcastThread"
							self.Stream.start()
						if Data == "C0":
							self.Stream.setCam(-1)
							Camera = 0
							logger.info("Client (%s, %s) has requested that no video stream be broadcasted." %Addr)
						else:
							indx = int(Data[1:2])
							if indx <= 0 or indx > 4:
								logger.error("Programming ERROR!")
								sys.exit()
							self.Stream.setCam(indx - 1)
							Camera = indx
							logger.info("Client (%s, %s)" % Addr + " has requested that the video stream for camera %d be broadcasted." % Camera)
					elif Data == "T" or Data == "T0" or Data == "T1" or Data == "T2":
						logger.info("Client (%s, %s) has requested that targeting start up." % Addr)
						self.Targeter = targetingmanager.TargetingManager(self.Conn, self.Addr)
						self.Targeter.daemon = True
						self.Targeter.name = "TargetingThread"
						self.Targeter.start()
						if Data == "T0":
							self.Targeter.setTarget(0)
							logger.info("Client (%s, %s) has requested that no alignment be made toward any target." %Addr)
						elif Data == "T1":
							self.Targeter.setTarget(1)
							logger.info("Client (%s, %s) has requested that alignment be made toward the high boiler opening." %Addr)
						elif Data == "T2":
							self.Targeter.setTarget(2)
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
