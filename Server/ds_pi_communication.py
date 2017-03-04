# ---------------------------------------------------------------------
# ds_pi_communication.py -- For transfering table data between Jetson and Driver Station
#
# Created 02/02/2017 K2, DLB, ...
# ---------------------------------------------------------------------

import socket
import time
import table_manners
import evsslogger

# Logging
logger = evsslogger.getLogger()

def run(Conn, Addr):
	Conn.settimeout(1)
	table = table_manners.readTable('/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
	table_manners.sendTable(Conn, table)
	while 1:
		data = Conn.recv(1024)
		if data == (b'\r\n' or b'null\r\n'):
			logger.debug ('in ds_pi_communication: ' + str(data))
			logger.debug ('null recieved in ds_pi_communication...')
			return
		data_str = str(data)

		# add a line here that checks the input such as:
		# if(table_manners.checkInput(data_str):
		key = table_manners.getKey(data_str)
		value = table_manners.getValue(data_str)

		table[key] = value
		table['timestamp'] = time.time()
		table_manners.writeTableToFile(table, '/home/ubuntu/epic/VisionSystem2017/Server/table_parameters.txt')
		print(table)
		table_manners.sendTable(Conn, table)

