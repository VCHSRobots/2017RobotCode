#
# VisionSystemServer. Created by: KJF, NG, TastyDucks
#

imPort base64, cv2, socket, threading, time
imPort ds_pi_communication, rio_pi_communication, imPort field_coordinates

#
#Global Variables
#

Host = "10.44.15.36"	# IP Address of the server-side processor
Port = 5800				# Port Address of server-side processor
RecvBuffer = 1024

def Echo(conn):
	string = conn.recv(1024)
	conn.send(string)
	ThreadMessage(string)

def ThreadMessage(message):
	#prints "THREAD_NAME: message"
	print(threading.current_thread().name + ': ' + str(message))

class ClientManager(threading.Thread):
	
	def __init__(self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr

	def run(self):
		ThreadMessage("New thread made for client (%s, %s)!" %addr)
		data = conn.recv(RecvBuffer)
		print (byteRequest)
		if byteRequest == (b'Requesting ds_pi_communication\r\n'):
			ds_pi_communication.run(conn, addr)
			ThreadMessage('Driverstation Program ended.  Closing Thread.')
			conn.close()
			return
		elif byteRequest == (b'Requesting rio_pi_communication\n'):
			conn.settimeout(1)
			rio_pi_communication.run(conn, addr)
			ThreadMessage('RoboRIO Program ended.  Closing Thread.')
			conn.close()
			return
		elif byteRequest == (b'Requesting field_coordinates\r\n'):
			field_coordinates.run(conn, addr)
			ThreadMessage('Field Coordinates Program ended.  Closing Thread.')
			conn.close()
			return
		else:
			ThreadMessage("Error in request.  Thread closing.")
			return
			
ServerManager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(.1)
ServerManager.bind((Host, Port))
ThreadMessage("Server manager socket created")

while 1:	
	ServerManager.listen(25)
	conn, addr = ServerManager.accept()
	new_client = ClientManager(conn, addr)
	new_client.start()
	ThreadMessage("New thread created")
	
