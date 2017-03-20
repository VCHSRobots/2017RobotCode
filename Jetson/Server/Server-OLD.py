#CameraSystem Server. Created by TastyDucks on 01/14/2017 for EPIC Robotz
#This program requires OpenCV 3.1.0+ and Python 3.4.0+!
import socket, time, select, cv2, numpy, base64

CONNECTION_LIST = []
RECV_BUFFER = 64
PORT = 5800 #Port to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(1) #Number of clients that may connect at one time
CONNECTION_LIST.append(server_socket)
Camera = 0

def broadcast_stream(Camera):
	FramesSent = 0
	Bin64Data = ""
	if Camera == 1:
		try:
			Cam = cv2.VideoCapture(0)
			log("[INFO] Ramping camera...")
			for i in xrange(10):
				ret, im = Cam.read()
				discard = im
			StartTime = time.time()
			while FramesSent < 30:
				try:
					ret, frame = Cam.read()
				except Exception as e:
					log("[FATL] Error taking image from camera: " + e + ".")
				try:
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				except Exception as e:
					log("[EROR] Failed to color image in grayscale:  " + e + ".")
				try:
					enc = cv2.imencode('.png', gray)[1]
					Bin64Data = base64.b64encode(enc)
				except Exception as e:
					log("[EROR] Error saving image file as binary data: " + e + ".")
				try:
					broadcast_data(Bin64Data)
				except Exception as e:
					log("[EROR] Unable to send image to client (%s, %s): " %addr + e + ".")
				FramesSent += 1
				log("[INFO] Frames sent: " + str(FramesSent) + "/30. Time elapsed is: " + str(time.time() - StartTime) + " seconds.")
		except:
			log("[EROR] Failed to send video stream for Camera 1 to client (%s, %s)" %addr + ".")
			Camera = 0
			socket.close()
			CONNECTION_LIST.remove(socket)
	elif Camera == 2:
		try:
			Cam = cv2.VideoCapture(1)
			log("[INFO] Ramping camera...")
			for i in xrange(10):
				ret, im = Cam.read()
				discard = im
			StartTime = time.time()
			while FramesSent < 30:
				try:
					ret, frame = Cam.read()
				except Exception as e:
					log("[FATL] Error taking image from camera: " + e + ".")
				try:
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				except Exception as e:
					log("[EROR] Failed to color image in grayscale:  " + e + ".")
				try:
					enc = cv2.imencode('.png', gray)[1]
					Bin64Data = base64.b64encode(enc)
				except Exception as e:
					log("[EROR] Error saving image file as binary data: " + e + ".")
				try:
					broadcast_data(Bin64Data)
				except Exception as e:
					log("[EROR] Unable to send image to client (%s, %s): " %addr + e + ".")
				FramesSent += 1
				log("[INFO] Frames sent: " + str(FramesSent) + "/30. Time elapsed is: " + str(time.time() - StartTime) + " seconds.")
		except:
			log("[EROR] Failed to send video stream for Camera 2 to client (%s, %s)" %addr + ".")
			Camera = 0
			socket.close()
			CONNECTION_LIST.remove(socket)
	elif Camera == 3:
		try:
			Cam = cv2.VideoCapture(2)
			log("[INFO] Ramping camera...")
			for i in xrange(10):
				ret, im = Cam.read()
				discard = im
			StartTime = time.time()
			while FramesSent < 30:
				try:
					ret, frame = Cam.read()
				except Exception as e:
					log("[FATL] Error taking image from camera: " + e + ".")
				try:
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				except Exception as e:
					log("[EROR] Failed to color image in grayscale:  " + e + ".")
				try:
					enc = cv2.imencode('.png', gray)[1]
					Bin64Data = base64.b64encode(enc)
				except Exception as e:
					log("[EROR] Error saving image file as binary data: " + e + ".")
				try:
					broadcast_data(Bin64Data)
				except Exception as e:
					log("[EROR] Unable to send image to client (%s, %s): " %addr + e + ".")
				FramesSent += 1
				log("[INFO] Frames sent: " + str(FramesSent) + "/30. Time elapsed is: " + str(time.time() - StartTime) + " seconds.")
		except:
			log("[EROR] Failed to send video stream for Camera 3 to client (%s, %s)" %addr + ".")
			Camera = 0
			socket.close()
			CONNECTION_LIST.remove(socket)
	elif Camera == 4:
		try:
			Cam = cv2.VideoCapture(3)
			log("[INFO] Ramping camera...")
			for i in xrange(10):
				ret, im = Cam.read()
				discard = im
			StartTime = time.time()
			while FramesSent < 30:
				try:
					ret, frame = Cam.read()
				except Exception as e:
					log("[FATL] Error taking image from camera: " + e + ".")
				try:
					gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				except Exception as e:
					log("[EROR] Failed to color image in grayscale:  " + e + ".")
				try:
					enc = cv2.imencode('.png', gray)[1]
					Bin64Data = base64.b64encode(enc)
				except Exception as e:
					log("[EROR] Error saving image file as binary data: " + e + ".")
				try:
					broadcast_data(Bin64Data)
				except Exception as e:
					log("[EROR] Unable to send image to client (%s, %s): " %addr + e + ".")
				FramesSent += 1
				log("[INFO] Frames sent: " + str(FramesSent) + "/30. Time elapsed is: " + str(time.time() - StartTime) + " seconds.")
		except:
			log("[EROR] Failed to send video stream for Camera 4 to client (%s, %s)" %addr + ".")
			Camera = 0
			socket.close()
			CONNECTION_LIST.remove(socket)
def log(msg):
	try:
		msg = time.strftime("%Y-%m-%d_%H:%M:%S") + " " + msg
		print(msg)
		with open("outlog.txt", "a") as file:
			file.write(msg + "\n")
	except Exception as e:
		print("[FATL] Error with logging system: " + e)
		print(msg)
def broadcast_data(message):
	for socket in CONNECTION_LIST:
		if socket != server_socket:
			try:
				socket.sendall(message + "\r\n")
			except Exception as e:
				log("[EROR] Failed to send message: " + message + ": to client (%s, %s)" %addr + ": " + e + ".")
				socket.close()
				CONNECTION_LIST.remove(socket)
def CommMan():
	log("[INFO] CameraSystem server initiated!")
	message = ""
	while True:
		CurrentTime = time.strftime("%Y-%m-%d_%H:%M:%S")
		read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
		for sock in read_sockets:
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				log("[INFO] Client (%s, %s) has connected." %addr)
			else:
				try:
					data = sock.recv(RECV_BUFFER)
					if data != "":
						if data.rstrip() == "C0":
							log("[INFO] Client (%s, %s) has requested that no camera data be transmitted." %addr)
						elif data.rstrip() == "C1":
							log("[INFO] Client (%s, %s) has requested that data for camera 1 be transmitted." %addr)
							broadcast_stream(1)
						elif data.rstrip() == "C2":
							log("[INFO] Client (%s, %s) has requested that data for camera 2 be transmitted." %addr)
							broadcast_stream(2)
						elif data.rstrip() == "C3":
							log("[INFO] Client (%s, %s) has requested that data for camera 3 be transmitted." %addr)
							broadcast_stream(3)
						elif data.rstrip() == "C4":
							log("[INFO] Client (%s, %s) has requested that data for camera 4 be transmitted." %addr)
							broadcast_stream(4)
						elif data.rstrip() == "1":
							log("[INFO] Client (%s, %s) has pinged this server." %addr)
						else:
							log("[EROR] Error parsing data recieved from client (%s, %s): " %addr + data + ": valid messages are: \"C0\", \"C1\", \"C2\", \"C3\", and \"C4\".")
					else:
						log("[INFO] Client (%s, %s) has disconnected." %addr)
						sock.close()
						CONNECTION_LIST.remove(sock)
				except Exception as e:
					log("[FATL] Error receiving data from client (%s, %s): Client considered disconnected: " %addr + str(e))
					sock.close()
					CONNECTION_LIST.remove(sock)
CommMan()
