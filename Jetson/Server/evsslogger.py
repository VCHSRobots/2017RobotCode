# ---------------------------------------------------------------------
# evsslogger.py -- Logger for Epic Vision System Server
#
# Created 02/25/17 DLB
#
# ---------------------------------------------------------------------

import logging
import cv2
import sys
import os, time

LogLocation = "/home/ubuntu/epic/server.log"

def getLogger():
  return logging.getLogger("EVSS")

# initLogging() -- initialize logger once by main line code.
def initLogging():
	os.environ['TZ'] = 'PDT'
	time.tzset()
	logger = logging.getLogger("EVSS")
	logger.setLevel(logging.DEBUG)
	hndler1 = logging.FileHandler(LogLocation)
	hndler2 = logging.FileHandler("/dev/stdout")
	hndler1.setLevel(logging.DEBUG)
	hndler2.setLevel(logging.DEBUG)
	fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%y%m%d-%H%M%S')
	hndler1.setFormatter(fmt)
	hndler2.setFormatter(fmt)
	logger.addHandler(hndler1)
	logger.addHandler(hndler2)
	logger.info("EPIC Vision System Server (EVSS) initiated!")
	logger.info("Running on Python version: " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]))
	logger.info("Running on OpenCV version: " + cv2.__version__ + ".")
