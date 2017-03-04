# ---------------------------------------------------------------------
# table_manners.py -- program to manage parameters table, read changes
#                  -- from driverstation, and deliver table to roboRio
#
# 02/02/2017 KJF Created
# ---------------------------------------------------------------------

import socket, threading, time

import evsslogger

# Logging
logger = evsslogger.getLogger()

# define function to check input format called checkInput(String)

def readTable(filename):
	f = open(filename, 'r')
	table = dict()
	for line in f:
		key = line[:line.find('=')].strip().lower()
		value = float(line[(line.find('=')+1):].strip())
		table[key] = value
	f.close()
	return table

def writeTableToFile(table, filename):
	f=open(filename, 'wt')
	for k, v in table.items():
		f.write(k + "=" + str(v) + '\n')
	f.close()

def getKey(line):
	# write this
	string = ''
	key = line[:line.find('=')].strip().lower()
	return key

def getValue(line):
	# write this
	value = 0.0
	try: value = float(line[(line.find('=')+1):].strip())
	except Exception as e:
		logger.debug("Invalid Value in getValue in table-manners.")
		value = 0
	return value

def sendTable(conn, table):
	for k, v in table.items():
		line = k + " = " + str(v) + "\n"
		byteLine = bytearray(line, 'utf-8')
		conn.send(byteLine)
	endLine = 'End of file\n'
	byteEndLine = bytearray(endLine, 'utf-8')
	conn.send(byteEndLine)
	logger.debug("End of file sent from sendTable.")
