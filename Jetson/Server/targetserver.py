# ---------------------------------------------------------------------
# targetserver.py -- Independant program to run Target System
#
# Created 3/15/17 DLB
# ---------------------------------------------------------------------

# This program is responsible for the following:
# 1. Launched at Startup and remain running no matter what.
# 2. Communicate with the laptop (driver station or "ds"), and send
#    a pic every 1 or 2 seconds that shows the status of the targeting system.
# 3. Receive adjustment commands for the driver station -- Save these to disk.
# 4. Produce pointing info and publish that via MQTT.
# 5. Decide on target to process based on messages from MQTT.

import paho.mqtt.client as mqtt 
import threading
import time
import pickle
import evsslogger

logger = evsslogger.getLogger()

paramfile = "/home/ubuntu/RobotCode2017/targetparams.pkl"
client = None
targtype = 0    # 0=none, 1=boiler, 2=peg.
targetparams = ['dummy' : 0]

def getparams()
	global targetparams

def save_params(obj, name ):
    with open(paramfile, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_params(name ):
    with open(paramfile, 'rb') as f:
        return pickle.load(f)

def saveparam(msg):
	key, val = string
	logger.info("New parameter to save: " + msg)
	


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("robot/ds/targetsystem/#")
	client.subscribe("robot/roborio/targetsystem/#")
	client.subscribe("robot/ds/ping")
	logger.info("MQTT Client connected.")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global targtype
	smsg = str(msg.payload).strip()
	if msg.topic == "robot/ds/targetsystem/mode" or msg.topic == "robot/roborio/targetsystem/mode":
		newtargtype = 0
		if smsg == 'none' or smsg == '0':
			newtargtype = 0
		elif smsg == 'boiler' or smsg == '1':
			newtargtype = 1
		elif smsg == 'peg' or smsg == '2':
			newtargtype = 2
		else:
			logger.error("Bad mode received on topic: " + msg.topic)
			newtargtype = 0
		if newtargtype != targtype:
			logger.info("Targeting Type change to: %d." % newtargtype)
		targtype = newtargtype
		client.publish("robot/jetson/targetsystem/mode", "%d" % targtype, 0, False)
	elif msg.topic == "robot/ds/targetsystem/param":
		saveparam(smsg)
	elif msg.topic == "robot/ds/ping":
		client.publish("robot/jetson/ping", str(msg.payload), 0, False)
		logger.info("Ping Response Sent for " + str(msg.payload))
	else:
		logger.info("Unprocessed message: " + msg.topic+" "+str(msg.payload))

def runit():
	global client
	evsslogger.initLogging("TargetSystem.log")
	logger.info("Starting Target System Server")

	client = mqtt.Client(client_id="JetsonTest", clean_session=True)
	client.on_connect = on_connect
	client.on_message = on_message
	client.max_inflight_messages_set(1)
	client.message_retry_set(2) # retries for QoS >1 messages
	client.connect("localhost", 5802, 60)

	while True:
		client.loop()
		#t = 0
		#if targtype > 0:
		#	Ans = targeter.getAnswer()   # Should get: (Frame, Type, Valid, X, Y)
		#else:
		#	Ans = (None, 0, False, 0, 0)
		#v = 1
		#if !Ans[2] :
		#	v = 0
		#it = Ans[1] - 1
		report = "%d, %d, %s, %d" % (targtype, 0, 0, 0)
		client.publish("robot/jetson/targetsystem/report", report)
		time.sleep(0.020)  # run Loop every 20 milliseconds

if __name__ == "__main__":
	runit()
