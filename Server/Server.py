# ---------------------------------------------------------------------
# Server.py -- Main Server for Jeston on 2017 EPIC Robot
#
# Created by: KJF, NG, TastyDucks, DLB
# ---------------------------------------------------------------------

from __future__ import print_function
from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback

#Below writen by epic team members:
import ds_pi_communication
import rio_pi_communication
import field_coordinates
import visionsystem
import targetcomm
import targeter
import evsslogger

# Logging
logger = evsslogger.getLogger()

#Internet

Host = "0.0.0.0"
Port = 5800
RecvBuffer = 1024
ClientBuffer = 16

#Misc

Targeter = None

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
		logger.info("Client (%s, %s) connected and situated." %Addr)

		try:
			Data = Conn.recv(RecvBuffer)
#			logger.debug("Recv'd data \"" + Data + "\" from client (%s, %s)." % Addr)
		except:
			logger.error("Error receiving data from client (%s, %s): Client considered disconnected:" %Addr)
			Conn.close()
			return
		try:
			if Data:
				Data = Data.rstrip()
				if Data == ("Requesting ds_pi_communication"):
					ds_pi_communication.run(Conn, Addr)
					Conn.close()
					logger.info("DS-To-Jetson comm closed.")
					return
				elif Data == ("Requesting rio_pi_communication"):
					rio_pi_communication.run(Conn, Addr)
					Conn.close()
					logger.info("RIO-To-Jetson communition closed.")
					return
				elif Data == ("Requesting field_coordinates"):
					field_coordinates.run(Conn, Addr)
					Conn.close()
					logger.info("RIO-To-Jetson field coordinates closed.")
					return
				elif Data == "C" or Data == "C0" or Data == "C1" or Data == "C2" or Data == "C3" or Data == "C4":
					visionsystem.run(Conn, Addr, Data)
					Conn.close()
					logger.info("Vision System closed.")
					return
				elif Data == "T" or Data == "T0" or Data == "T1" or Data == "T2":
					targetcomm.run(Conn, Addr, Data, Targeter)
					Conn.close()
					logger.info("Target System closed.")
					return
				else:
					logger.error("Error parsing command recieved from client (%s, %s) \"" % Addr + Data + "\".")
					Conn.close()
					return
			else:
				logger.info("Client (%s, %s) has disconnected." %Addr)
				Conn.close()
				return
		except:
			logger.error("Unexpected Exception from low level code! -- Closing Connection...")
			traceback.print_exc()
			Conn.close()
			return

#
#Begin mainline code
#

if __name__ == "__main__":
	global Targeter
	evsslogger.initLogging()
	ServerManager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	time.sleep(0.1)
	ServerManager.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	ServerManager.bind((Host, Port))
	NumberOfClientThreads = 0
	logger.info("Starting Main EPIC Robot Server for the Jetson")
	Targeter = targetingmanager.TargetingManager()
	Targeter.daemon = True
	Targeter.name = "TargetingManager"
	Targeter.start()

	while True:
		ServerManager.listen(ClientBuffer)
		Conn, Addr = ServerManager.accept()
		NewClient = ClientManager(Conn, Addr)
		NumberOfClientThreads += 1
		NewClient.name = "ClientThread:" + str(NumberOfClientThreads)
		NewClient.daemon = True
		NewClient.start()
		logger.info("New Client Connection Started: (%s, %s)" % Addr)
