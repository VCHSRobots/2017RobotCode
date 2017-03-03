# -------------------------------------------------------
# mousetst.py -- program to read mouse 
#
# 01/27/17 DLB Created
# -------------------------------------------------------



f = open("/dev/hidraw2", "rb")

while True:
	c = f.read(8)
	cc = []
	for i in c:
		cc.append(ord(i))
	ccc = tuple(cc)
	print("%3d %3d %3d %3d %3d %3d %3d %3d" % ccc)

"""

Notes:

Works in 8 columns of bytes.

A, B, C, D, E, F, G, H

A is button presses - 2 (left click), 4 (right click), 6 (wheel press), 8 (side button 1), 16 (side button 2)
B, E, and F are left-to-right motion. 255 on all for left, AND 1 for B & E, 0 on F for right

"""
