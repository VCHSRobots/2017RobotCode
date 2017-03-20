# -------------------------------------------------------
# findRazerMouse.py -- Find the device for the Razer mouse.
#
# 03/03/17 DLB Created
# -------------------------------------------------------


#NOTE: the package 'pyudev' must be installed with >pip install pyudev

## NOTE: To read from the returned mouse device, without special privilages,
## you must edit the udev files as follows:  Add a file under /etc/udev/ 
## named: 99-hidraw-permissions.rules.  In that file, put this line:
##   KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="robot"
## then reboot the system.

import pyudev
import shlex
from subprocess import Popen, PIPE
import string as str

def findRazer():
	# First, get a list of all usb devices to see if it is plugged in.
	cmd = "lsusb"
	process = Popen(shlex.split(cmd), stdout=PIPE) 
	usblist, dummy  = process.communicate()
	ok = process.wait()
	if ok != 0:
		return None
	listelements = usblist.split('\n')
	device_info = None
	for usbdevice in listelements:
		if usbdevice.find("Razer") > 0:
			device_info = usbdevice
			break
	if device_info is None:
		return None
	idx = device_info.find(" ID ")
	if idx <= 0:
		return None
	device_id = device_info[idx+4:idx+13]
	# We now have the USB device ID. Match this with a hidraw dev...
	ctx = pyudev.Context()
	for sdev in ctx.list_devices():
		if str.find(sdev.sys_path, "hidraw") > 0:
			if str.find(sdev.sys_path, device_id) > 0:
				return "/dev/" + sdev.sys_name
	return None

if __name__ == "__main__":
	dev = findRazer()
	if dev is not None:
		print("Device Found = " + dev)
	else:
		print("Device NOT found.")


