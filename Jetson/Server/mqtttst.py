# ---------------------------------------------------------------------
# mqtttst.py -- Testing MQTT for comm
#
# Created 3/15/17 DLB
# ---------------------------------------------------------------------

import paho.mqtt.client as mqtt
import threading
import time

pingtime = 0
client = None
cnt = 0
oldpingtime = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("robot/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	if msg.topic == "robot/pingtest":
		client.publish("robot/jetson/ping", str(msg.payload), 0, False)
		print("Ping Response Sent for " + str(msg.payload))
	elif msg.topic == "robot/jetson/pingback":
		elptime = time.time() - pingtime
		print("Self Ping Time = %9.6f seconds" % elptime)
	elif msg.topic == "robot/JavaLaptop/ping":
		client.publish("robot/Jetson/javapingresponse", "dummy", 0, False)
		print("Responded to JavaLaptop ping. " + str(msg.payload))
	else:
		print(msg.topic+" "+str(msg.payload))

def counter():
	global cnt
	global client
	global pingtime
	global oldpingtime
	while True:
		cnt += 1
		if client is not None:
			pingtime = time.time()
			if oldpingtime != 0:
				elp = pingtime - oldpingtime
				print("elp of counter = %12.4f seconds" % elp)
			oldpingtime = pingtime
			spingtime = "%d" % pingtime
			client.publish("robot/jetson/pingtest", spingtime, 0, True)
		time.sleep(2.5)
		print("Counter = %d" % cnt)

def runit():
	global client
	client = mqtt.Client(client_id="JetsonTest", clean_session=True)
	client.on_connect = on_connect
	client.on_message = on_message
	client.max_inflight_messages_set(1)
	client.message_retry_set(2) # retries for QoS >1 messages
	client.connect("localhost", 5802, 60)
	client.loop_forever();
#	while True:
#		client.loop()
#		time.sleep(0.0020)  # run Loop every 2 milliseconds

if __name__ == "__main__":
	count_thread = threading.Thread(target=counter)
	count_thread.daemon = True
	count_thread.name ="CounterThread"
	count_thread.start()
	runit()



