# ---------------------------------------------------------------------
# field_coordinates.py -- Field Coordinates Reader for EPIC Robot 2017
#
# Created by: KJF, NG, TastyDucks, DLB
# ---------------------------------------------------------------------

import socket
import math
import mouse_reader_jetson
import time
import sys
import evsslogger

# Logging
logger = evsslogger.getLogger()

try:
	mouse_reader_jetson.initMouseTrack()
except:
	logger.error("Mouse Reader Init failed")

def run(conn, addr):
	logger.info("Starting Field Coordinates")
	xm1 = 0.0
	ym1 = 0.0
	xf0 = 0.0
	yf0 = 0.0
	xf1 = 0.0
	yf1 = 0.0
	conn.send("field_coordinates request recv'd\n")
	while True:
		xm0 = xm1
		ym0 = ym1
		xf0 = xf1
		yf0 = yf1
		conn.settimeout(1)
		try:
			data = conn.recv(1024)				# waiting for gyro angle	
			logger.debug("gyro angle recieved.")
		except socket.timeout:
			logger.error('Socket timed out at gyro angle read operation')
			break
		if not data: 
				break		
		else:
			theta = float(data)
		try:
			xm1, ym1, okay = mouse_reader_jetson.getMousePosition()
			logger.debug("Mouse positions = %7.3f %7.3f " % (xm1, ym1) + str(okay))
		except:
			logger.error("Get Mouse Position function failed")
		deltaXm = xm1 - xm0
		deltaYm = ym1 - ym0
		if (deltaYm < 0):
			theta = theta + 180
			deltaYm = deltaYm * -1.0
			deltaXm = deltaXm * -1.0
		if (deltaYm == 0):
			alpha = -1.0 * theta
		else:
			alpha = 90.0 - theta - math.degrees(math.atan((deltaXm) / (deltaYm)))

		# is atan returning in radians or degrees?
		if (deltaYm == 0.0 and deltaXm < 0.0):
			xf1 = xf0 - math.sqrt((deltaXm)**2 + (deltaYm)**2) * math.cos(math.radians(alpha))
		else:
			xf1 = xf0 + math.sqrt((deltaXm)**2 + (deltaYm)**2) * math.cos(math.radians(alpha))
			yf1 = yf0 + math.sqrt((deltaXm)**2 + (deltaYm)**2) * math.sin(math.radians(alpha))
			sxf1 = "%15.6f\n" % xf1
		syf1 = "%15.6f\n" % yf1
		bxf1 = bytearray(sxf1, 'utf-8')
		byf1 = bytearray(syf1, 'utf-8')
		logger.debug("sending x data")
		conn.send(bxf1)
		try:
			print(conn.recv(1024))
		except socket.timeout:
			logger.error('Socket timed out at X field recv operation')
			break
		logger.debug("sending y data")
		conn.send(byf1)

		logger.debug('alpha = ' + str(alpha) + '   xf1 = ' + str(xf1) + '   yf1 = ' + str(yf1))
	conn.close()
	logger.debug('Field Coordinate Loop Exited.')		
