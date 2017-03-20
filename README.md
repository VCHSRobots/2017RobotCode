# RobotCode2017

This code was developed by FRC Team 4415 for the 2017 game, "FIRST Steamworks"

It consists of code for the RoboRio writen in java, and code for the Jetson TX1,
writen in python.  There is also dashboard code that runs on a laptop that is
written in C# and Java.  

The various processors communitate over the network (LAN) with a custom socket protocol.  In
addition, we started using MQTT right before the end of the season.  The Jetson runs a
Mosquitto broker and the various programs publish and receive data from the broker.  

We use a static IP scheme.  Our RoboRio is 10.44.15.2.  Our Jetson is 10.44.15.19.  
We use port 5800 for our custom protocol, and port 5802 for the MQTT protocol.

The Jetson maintains the MQTT data, but its main job is for vision processing.  We have
two cameras connected to the Jetson (Microsoft HD 3000 USB cameras).  One looks forward
at the boiler, and the other looks backward at the peg.  The Jetson reports (vis MQTT topics)
the offset to the target from the center of the pictures.  It also calculates range based
on the size of the targets.



