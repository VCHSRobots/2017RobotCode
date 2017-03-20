# ---------------------------------------------------------------------
# sendmqttmsg.py -- Simple command line program to send a MQTT message
#
# Created 3/19/17 DLB
# ---------------------------------------------------------------------

import paho.mqtt.client as mqtt
import threading
import time
import sys

pingtime = 0
client = None
topic = ""
message = ""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.publish(sys.argv[1], sys.argv[2], 0, False)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print("From Server: " + msg.topic+" "+str(msg.payload))

def main():
	if len(sys.argv) < 3:
		print("Not enough args: Use python sendmqtt topic msg")
		sys.exit(1)
	global topic
	global message
	topic = sys.argv[1]
	message = sys.argv[2]
	print("Sending Topic: " + topic)
	print("Message: " + message)
	client = mqtt.Client(client_id="JetsonSendOnce", clean_session=True)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 5802, 10)
	client.loop()
	time.sleep(1)


if __name__ == "__main__":
	main()


