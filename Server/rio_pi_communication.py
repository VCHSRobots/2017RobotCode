# ---------------------------------------------------------------------
# rio_pi_communication.py -- For transfering table data between Jetson and RoboRio
#
# Created 02/02/2017 K2, DLB, ...
# ---------------------------------------------------------------------

import socket
import time
import table_manners
import datetime
import evsslogger

# Logging
logger = evsslogger.getLogger()

def run(conn, addr):
	try:
		conn.settimeout(1)
		logger.info('Sending table request response...')
		conn.send(bytearray('Request granted\n','utf-8'))
		logger.info('Table request response sent...')
		itsreports = 0
		ittabreports = 0
	except:
		logger.error("RoboRIO IO error on initial requests... Restarting")
		return
	while 1:
		try:
			data = conn.recv(1024)
		except socket.timeout:
			logger.info('RoboRIO Connection timed out in Table Request. Restarting')
			conn.close()
			return
		except socket.error:
			logger.info("RoboRIO Connection error in Table Request. Restarting.")
			conn.close()
			return
		if data == (b'Requesting table\n' or b'Requesting table\r\n'):
			table = table_manners.readTable('/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
			table['timestamp'] = time.time()
			table_manners.writeTableToFile(table, '/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
			table_manners.sendTable(conn, table)
			ittabreports += 1
			if ittabreports % 10:
				logger.info("Full tables sent: %d", ittabreports)
		if data == (b'Requesting timestamp\n' or b'Requesting timestamp\r\n'):
			table = table_manners.readTable('/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
			timestamp = table['timestamp']
			stringtimestamp = str(timestamp) + '\n'
			bytetimestamp = bytearray(stringtimestamp, 'utf-8')
			conn.send(bytetimestamp)
			itsreports += 1
			if itsreports % 50 == 0:
				logger.info("Table Data Timestamp reports = %d", itsreports)
		if data == (b'\r\n' or b'null\r\n'):
				logger.info("Illegal cmd from RoboRio in rio_pi_communcaiton.  Null received.")
				break
