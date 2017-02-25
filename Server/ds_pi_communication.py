import socket
import time
import table_manners

def run(conn, addr):
	table = table_manners.readTable('/home/pi/Desktop/2.7 Robot Communication/table_parameters.txt')
	table_manners.sendTable(conn, table)
	while 1:
		data = conn.recv(1024)
		if data == (b'\r\n' or b'null\r\n'):
			print (str(data))
			print ('null recieved.')
			return
		data_str = str(data)
		
		# verify that the input is in the proper form
		key = table_manners.getKey(data_str)
		value = table_manners.getValue(data_str)
		
		table[key] = value
		table['timestamp'] = time.time()
		table_manners.writeTableToFile(table, '/home/pi/Desktop/2.7 Robot Communication/table_parameters.txt')
		print(table)
		table_manners.sendTable(conn, table)

