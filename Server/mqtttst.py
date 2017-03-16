# ---------------------------------------------------------------------
# mqtttst.py -- Testing MQTT for comm
#
# Created 3/15/17 DLB
# ---------------------------------------------------------------------

import paho.mqtt.client as mqtt
import threading
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("robot/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))


client = None
cnt = 0

def counter():
	global cnt
	global client
	while True:
		cnt += 1
		if client is not None:
			client.publish("robot/tstcount", "%d" % cnt, 0, True)
		time.sleep(2.5)
		print("Counter = %d" % cnt)

def runit():
	global client
	client = mqtt.Client(client_id="JetsonTest", clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("localhost", 5802, 60)
	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	while True:
		client.loop()
		time.sleep(0.020)  # run Loop every 20 milliseconds
		#	client.loop_forever()

if __name__ == "__main__":
	count_thread = threading.Thread(target=counter)
	count_thread.daemon = True
	count_thread.name ="CounterThread"
	count_thread.start()
	runit()



