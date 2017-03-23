#Program for demonstrating autoaiming. Created TastyDucks 3/18/17

import sys
import cv2
import evsslogger
import targeter
from subprocess import call
import traceback
import time

logger = evsslogger.getLogger()
evsslogger.initLogging()

if len(sys.argv) > 1:
	Input = sys.argv[1]
	if len(sys.argv) > 2:
		logger.info("Ignoring extra value input after first perameter in command call...")
else:
	logger.warn("Invalid input! No target index specified when command was called. (Examples of valid calls: \"python targetingdemo.py 0\", or \"python targetingdemo.py 1\".)\r\nInput set to default of \"0\".")
	Input = "0"

Targeter = targeter.Targeter()
Targeter.daemon = True
Targeter.name = "Targeter"
Targeter.setTarget(int(Input))

Cam = None

if Input == "0":
	logger.info("Starting demo for target \"0\" (HIGH BOILER)...")
	time.sleep(1)
	try:
		call(["v4l2-ctl", "-c", "exposure_auto=1"])
		call(["v4l2-ctl", "-c", "exposure_absolute=5"])
		call(["v4l2-ctl", "-c", "brightness=30"])
		Cam = cv2.VideoCapture(0)
	except:
		logger.error("Unable to setup Cam 0 for capture.")
		traceback.print_exc()
	if Cam:
		while True:
			Return = Targeter.GetTarget(Cam, 0)
			logger.info("Return data: " + str(Return[1:]))
			cv2.imshow("Targeting Data Image:", Return[0])
			cv2.waitKey(1)
elif Input == "1":
	logger.info("TARGETING DEMO: Starting demo for target \"1\" (GEAR DELIVERY)...")
	time.sleep(1)
	try:
		call(["v4l2-ctl", "--device=2", "-c", "exposure_auto=1"])
		call(["v4l2-ctl", "--device=1", "-c", "exposure_absolute=5"])
		call(["v4l2-ctl", "--device=1", "-c", "brightness=30"])
		Cam = cv2.VideoCapture(1)
	except:
		logger.error("Unable to setup Cam 0 for capture.")
		traceback.print_exc()
	if Cam:
		while True:
			Return = Targeter.GetTarget(Cam, 1)
			logger.info("Return data: " + str(Return[1:]))
			cv2.imshow("Targeting Data Image:", Return[0])
			cv2.waitKey(1)
else:
	print("TARGETING DEMO ERROR: Invalid input \"" + str(Input) + "\"! Valid target indexes are \"0\" (HIGH BOILER), and \"1\" (GEAR DELIVERY).")

