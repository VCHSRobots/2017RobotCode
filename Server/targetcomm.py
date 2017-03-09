# ---------------------------------------------------------------------
# targetcomm.py -- Target communication system for epic 2017 robot
#
# Created 03/03/2017 TastyDucks, DLB
# ---------------------------------------------------------------------

from __future__ import print_function
from subprocess import call
import base64, cv2, socket, sys, threading, time, traceback

#Below writen by epic team members:
import evsslogger
import targeter
Targeter = None
RecvBuffer = 1024

# Logging
logger = evsslogger.getLogger()

"""
class TarSysDummy:
	def __init__(self):
		self.targetindex = 0
		self.iDumCount = 0
	def start(self):
		return 0
	def setTarget(self, targetindex):
		self.targetindex = targetindex
	def GetResults(self):
		time.sleep(0.04)
		self.iDumCount += 1
		return "%2d, Valid, %d, %d" % (self.targetindex, self.iDumCount, self.iDumCount*5)
"""

def run(Conn, Addr, Data, Targeter):
	logger.info("Client (%s, %s) has requested that targeting start up." % Addr)
	iCount = 0
	if Data == "T0":
		Targeter.setTarget(-1)
		logger.info("Client (%s, %s) has requested that no alignment be made toward any target." % Addr)
	elif Data == "T1":
		Targeter.setTarget(0)
		logger.info("Client (%s, %s) has requested that alignment be made toward the high boiler opening." % Addr)
	elif Data == "T2":
		Targeter.setTarget(1)
		logger.info("Client (%s, %s) has requested that alignment be made toward the gear delivery peg." % Addr)
	while True:
		out = Targeter.getAnswer()
		sout = (str(out) + '\n')
		try:
			byteout = bytearray(sout, 'utf-8')
			Conn.send(byteout)
		except:
			logger.error("Error sending Target data to client (%s, %s): Client considered disconnected:" % Addr)
			#Close targeting thread here
			Conn.close()
			return
		iCount += 1
		if iCount % 250 == 0:
			logger.info("Number of target reports sent: %d (type=%s)" % (iCount, Data))

