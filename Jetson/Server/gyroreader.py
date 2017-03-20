from sense_hat import SenseHat
import time
import socket
#import gyrodata
import sys

host = '10.44.15.35'
port = 5800
startTime = time.time()

def keepTime(startTime):
	while 1:
		elapsedTime = (time.time() - startTime)
		return(elapsedTime)


#gyro_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#gyro_socket.bind((host, port))
#print('Socket created')
#print('Listening...')
#gyro_socket.listen(1)
#conn, addr = gyro_socket.accept()
#print ("Connected with " + addr[0] + ":" + str(addr[1]))
#gyrodata.initGetGyroAngle()
while 1:
	elapsedTime = keepTime(startTime)
	gyroAngle = 269.01532#gyrodata.getGyroData()
	gyroAngleString = ("Found angle: " + str(gyroAngle) + " ")
	elapsedTimeString = ("in time: " + str(elapsedTime))
	print (gyroAngleString + elapsedTimeString)
#	data = conn.recv(1024)
#	print (str(data))
#	if data == (b'Requesting Gyro\r\n'):
#		gyrodata.sendGyroData(conn)

#conn.close
