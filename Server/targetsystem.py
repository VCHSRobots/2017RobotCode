# ---------------------------------------------------------------------
# targetsystem.py -- Target system for epic 2017 robot
#
# Created 03/03/2017 TastyDucks, DLB
# ---------------------------------------------------------------------

from __future__ import print_function
from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback

#Below writen by epic team members:
import evsslogger
import targetingmanager

RecvBuffer = 1024

# Logging
logger = evsslogger.getLogger()

def run(Conn, Addr, Data):
	logger.info("Client (%s, %s) has requested that targeting start up." % Addr)
	Targeter = targetingmanager.TargetingManager(Conn, Addr)
	Targeter.daemon = True
	Targeter.name = "TargetingThread"
	Targeter.start()
	while True:
		if Data == "T0":
			Targeter.setTarget(-1)
			logger.info("Client (%s, %s) has requested that no alignment be made toward any target." % Addr)
		elif Data == "T1":
			Targeter.setTarget(0)
			logger.info("Client (%s, %s) has requested that alignment be made toward the high boiler opening." % Addr)
		elif Data == "T2":
			Targeter.setTarget(1)
			logger.info("Client (%s, %s) has requested that alignment be made toward the gear delivery peg." % Addr)
			try:
				Data = Conn.recv(RecvBuffer)
			except:
				logger.error("Error receiving data from client (%s, %s): Client considered disconnected:" % Addr)
				Conn.close()
				return

