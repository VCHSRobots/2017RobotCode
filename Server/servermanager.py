# -----------------------------------------------------------------
# servermanager.py -- program to accept clients on separate threads
#
# 01/31/17 NG Created
# -----------------------------------------------------------------
#python libraries
import socket
import threading
import time
#network libraries
import ds_pi_communication
import rio_pi_communication
#mouse libraries
#import field_coordinates

def echo(conn):
	string = conn.recv(1024)
	conn.send(string)
	threadMessage(string)

def threadMessage(message):
	#prints "THREAD_NAME: message"
	print(threading.current_thread().name + ': ' + str(message))

class ClientManager(threading.Thread):
	
	def __init__(self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr

	def run(self):
		threadMessage("New thread made for client (%s, %s)!" %addr)
		byteRequest = conn.recv(1024)
		request = str(byteRequest)
		print (byteRequest)
		if byteRequest == (b'Requesting ds_pi_communication\r\n'):
			ds_pi_communication.run(conn, addr)
			threadMessage('Driverstation Program ended.  Closing Thread.')
			conn.close()
			return
		elif byteRequest == (b'Requesting rio_pi_communication\n'):
			conn.settimeout(1)
			rio_pi_communication.run(conn, addr)
			threadMessage('RoboRIO Program ended.  Closing Thread.')
			conn.close()
			return
		elif byteRequest == (b'Requesting field_coordinates\r\n'):
			field_coordinates.run(conn, addr)
			threadMessage('Field Coordinates Program ended.  Closing Thread.')
			conn.close()
			return
		else:
			threadMessage("Error in request.  Thread closing.")
			return

host = '10.44.15.16'	# IP Address of the server-side processor
port = 5800				# Port Address of server-side processor

server_manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(.1)
server_manager.bind((host, port))
threadMessage("Server manager socket created")

while 1:	
	server_manager.listen(25)
	conn, addr = server_manager.accept()
	new_client = ClientManager(conn, addr)
	new_client.start()
	threadMessage("New thread created")
	
