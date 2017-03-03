# -------------------------------------------------------
# mouse_reader_jetson.py -- program to read mouse locations on the Jetson
#
# 01/27/17 DLB Created
# -------------------------------------------------------
import threading
import findRazerMouse
import time

xloc = 0.0          #  X location in inches
yloc = 0.0          #  Y location in inches
fmsefile = 0        #  file handle for the mouse device
msescale = 1000.0   #  pixels per inch

MouseOpen = False
DeviceName = None

def sumMovement(x, y):
	global xloc, yloc
	x_ord = ord(x)
	y_ord = ord(y)
	if x_ord >= 128:
		x_ord = x_ord - 256
	if y_ord >= 128:
		y_ord = y_ord - 256
	xloc += float(x_ord) / msescale
	yloc += float(y_ord) / msescale

def readMsePosition():
	global fmsefile, xloc, yloc
	if MouseOpen is None:
		return 0, 0, False
	c = fmsefile.read(8)
	n = len(c)
	if n != 8:
		print('Mouse Read Error! Missed Bytes.')
		return xloc, yloc, False
	sumMovement(c[1], c[2])
	return xloc, yloc, True

def runmseread():
	while True:
		time.sleep(0.01)
		readMsePosition()

def initMouseTrack():
	global fmsefile, xloc, yloc
	xloc = 0
	yloc = 0
	DeviceName = findRazerMouse.findRazer()
	if DeviceName is None:
		MouseOpen = False
		return
	fmsefile = open(DeviceName, "rb")
	MouseOpen = True
	t = threading.Thread(target=runmseread)
	t.daemon = True
	t.start()

def getMousePosition():
	global xloc, yloc
	if not MouseOpen:
		return 0,0, False
	return xloc, yloc, True

def getMouseDeviceName():
	return DeviceName

if __name__ == "__main__":
	initMouseTrack()
	while True:
		x, y, okay = readMsePosition()
		if not okay:
			print("Mouse Read Error!")
		else:
			print ("x, y = %8.3f, %8.3f" % (x, y))
