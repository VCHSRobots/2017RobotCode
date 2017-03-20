from sense_hat import SenseHat
import threading
import time

sense = SenseHat()
orientation = sense.get_orientation()
gyroAngle = orientation['yaw']

def runGyroRead():
	global gyroAngle
	while True:
		orientation = sense.get_orientation()
		sense.set_imu_config(False, True, False)
		gyroAngle = orientation['yaw']
		time.sleep(.005)
		

def initGetGyroAngle():
	t = threading.Thread(target=runGyroRead)
	t.start()

def getGyroData():
	global gyroAngle
	sense.set_imu_config(False, True, False)
	orientation = sense.get_orientation()
	gyroAngle = orientation['yaw']
	return gyroAngle

def sendGyroData(conn):
	global gyroAngle
	str_gyroAngle = str(gyroAngle) + '\n'
	byteAngle = bytearray(str_gyroAngle, 'utf-8')
	print(byteAngle)
	conn.send(byteAngle)
	print('data sent')
	
