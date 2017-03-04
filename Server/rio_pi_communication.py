# ---------------------------------------------------------------------
# rio_pi_communication.py -- For transfering table data between Jetson and RoboRio
#
# Created 02/02/2017 K2, DLB, ...
# ---------------------------------------------------------------------

import socket
import time
import table_manners
import datetime

def run(conn, addr):
	conn.settimeout(1)
	print ('sending response...')
	conn.send(bytearray('Request granted\n','utf-8'))
	print ('response sent...')
	while 1:
		try:
			data = conn.recv(1024)
		except socket.timeout:
			print ('RoboRIO Connection timed out.')
			conn.close()
			return
		if data == (b'Requesting table\n' or b'Requesting table\r\n'):
			table = table_manners.readTable('/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
			table['timestamp'] = time.time()
			table_manners.writeTableToFile(table, '/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
			table_manners.sendTable(conn, table)
		if data == (b'Requesting timestamp\n' or b'Requesting timestamp\r\n'):
			table = table_manners.readTable('/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
			timestamp = table['timestamp']
			stringtimestamp = str(timestamp) + '\n'
			bytetimestamp = bytearray(stringtimestamp, 'utf-8')
			conn.send(bytetimestamp)
		if data == (b'\r\n' or b'null\r\n'):
				print(str(data))
				print('null recieved.')
				break
