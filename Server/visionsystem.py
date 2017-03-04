# ---------------------------------------------------------------------
# visionsystem.py -- vision system to send pics to Driver Station
#
# Created 03/03/2017 Tasty Ducts, DLB
# ---------------------------------------------------------------------

from __future__ import print_function
from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback

#Below writen by epic team members:
import evsslogger
import camerastream

RecvBuffer = 1024

# Logging
logger = evsslogger.getLogger()

def run(Conn, Addr, Data):
	logger.info("Client (%s, %s) has requested that the vision system be started up." % Addr)
	Stream = camerastream.BroadcastStream(Conn, Addr)
	Stream.daemon = True
	Stream.name = "BroadcastThread"
	Stream.start()
	while True:
		if Data == "C0":
			Stream.setCam(-1)
			Camera = 0
			logger.info("Client (%s, %s) has requested that no video stream be broadcasted." % Addr)
		else:
			indx = int(Data[1:2])
			if indx <= 0 or indx > 4:
				logger.error("Programming ERROR!")
				indx = 1
			Stream.setCam(indx - 1)
			Camera = indx
			logger.info("Client (%s, %s)" % Addr + " has requested that the video stream for camera %d be broadcasted." % Camera)
		try:
			Data = Conn.recv(RecvBuffer)
		except:
			logger.error("Error receiving data from client (%s, %s): Client considered disconnected:" %Addr)
			Conn.close()
			return
