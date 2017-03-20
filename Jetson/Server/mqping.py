# ---------------------------------------------------------------------
# mqping.py -- Testing MQTT for comm
#
# Created 3/15/17 DLB
# ---------------------------------------------------------------------

import paho.mqtt.client as mqtt
import threading
import time

client = None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("robot/jetson/pingtest")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic == "robot/jetson/pingtest":
		client.publish("robot/jetson/pingback", str(msg.payload), 0, False)
		print("Ping Response Sent for " + str(msg.payload))
	else:
		print("Unknown topic: " + msg.topic+" "+str(msg.payload))

def runit():
	global client
	client = mqtt.Client(client_id="JetsonTest2", clean_session=True)
	client.on_connect = on_connect
	client.on_message = on_message
	client.max_inflight_messages_set(1)
	client.message_retry_set(2) # retries for QoS >1 messages
	client.connect("localhost", 5802, 60)
	client.loop_forever();

if __name__ == "__main__":
	runit()

