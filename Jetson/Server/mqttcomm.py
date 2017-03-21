# ---------------------------------------------------------------------
# mqttcomm.py -- MQTT comm module for the 2017 robot (Runs on the Jetson)
#
# Created 3/21/17 DLB
# ---------------------------------------------------------------------

# This module provides a public API to send and receive MQTT messages.
# It runs on it's own thread.

import sys
import paho.mqtt.client as mqtt
import threading
import time
import evsslogger

logger = evsslogger.getLogger()

client = None
nCountMsgIn = 0
nCountMsgOut = 0
incomingMsgLock = threading.Lock()
incomingMsgs = {}  # A dick of the latest received messages.  topic is the key.

#returns a count of messages received since startup
def getCountMsgIn():
	return nCountMsgIn;

#returns a count of messages published by us since startup
def getCountMsgOut():
	return nCountMsgOut;

#sends a message on the next output cycle.
def send(topic, text):
	#Here, we assume that the mqtt stuff handles the thread.
	if client is not None:
		client.publish(topic, text, 0, True)
	else:
		logger.warn("MQTTCom: Client is NONE on send.")

#returns a dict of all messages currently received
def getAllMessages():
	global incomingMsgLock
	outmsgs = {}
	incomingMsgLock.acquire()
	for x in incomingMsgs:
		outmsgs[x] = incomingMsgs[x]
	incomingMsgLock.release()
	return outmsgs

#returns the latest message on a given topic
def getMessage(topic):
	incomingMsgLock.acquire()
	if topic in incomingMsgs:
		v = incomingMsgs[topic]
	else:
		v = None
	incomingMsgLock.release()
	return v

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	logger.info("MQTT: Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("robot/ds/#")
	client.subscribe("robot/roborio/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global incomingMsgs
	global nCountMsgIn
	nCountMsgIn += 1
	incomingMsgLock.acquire()
	incomingMsgs[msg.topic] = str(msg.payload).strip()
	incomingMsgLock.release()

# The callback for when our messages are actually published at the broker.
def on_publish(client, userdata, mid):
	global nCountMsgOut
	nCountMsgOut += 1

# Runs in the background, while at all times tries to keep the connection
# up and running.  Checks to send new messages once every 20ms.
#
# NOTE: Not being used... using loop_start() instead which provides
# the same functionallity (we hope) as the code below.
def run_in_background(name, host, port):
	global client
	while(true):
		try:
			client = mqtt.Client(client_id=name, clean_session=True)
			client.on_connect = on_connect
			client.on_message = on_message
			client.on_publish = on_publish
			client.max_inflight_messages_set(10)
			client.message_retry_set(2) # retries for QoS >1 messages
			client.connect(host, port, 60)
			while true:
				client.loop()
				sendRawMsgs()
				time.sleep(0.020)
		except:
			logger.error("MQTTCom: lost clinet connection.  Retrying.")
			time.sleep(0.200)

# Starts the MQTT client running in the background.  After this, you
# call call send or receive.
def start(OurName):
	global client
	try:
		client = mqtt.Client(client_id=OurName, clean_session=True)
		client.on_connect = on_connect
		client.on_message = on_message
		client.on_publish = on_publish
		client.max_inflight_messages_set(10)
		client.message_retry_set(2) # retries for QoS >1 messages
		client.connect("localhost", 5802, 60)
		client.loop_start()
	except:
		logger.error("MQTTCom: Unable to aquire client. Aborting.")

	#Old Code to run our own background loop:
    #t = Thread(target=run_in_background, args=(OurName, "localhost", 5802))
	#t.daemon = True
	#t.name = "MQTTComm"
    #t.start()

if __name__ == "__main__":
	evsslogger.initLogging("Dummy.log")
	start("JetsonTestComm")
	while True:
		cmd = raw_input("mqtt_tst. q=quit, x=list, s=stats, topic:text = send msg> ")
		cmd = cmd.strip()
		if len(cmd) <= 0:
			continue
		if cmd == "q":
			sys.exit()
		elif cmd == "x":
			msgs = getAllMessages()
			for x in msgs:
				print("  %40s : %s\n" % (x, msgs[x]))
		elif cmd == "s":
			print("Number of Msg Sent: %d" % getCountMsgOut())
			print("Number of Msg Received: %d" % getCountMsgIn())
		else:
			indx = cmd.find(":")
			if indx <= 0:
				print("Syntax error. Message Not Sent")
				continue
			topic = cmd[0:indx]
			val = cmd[indx+1:]
			send(topic,val)

