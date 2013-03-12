import sys
import struct

def createPDU(data = [0]):
	# data is a list
	if data[0] == 3:
		#return "Read"
		return data
	elif data[0] == 16:
		return "Write"
	else:
		return "Invalid Function Number!"
	#PDU = data
	#return PDU

def PDUReadHoldingRegisters():
	#Create Read Holding Registers
	return 1

def PDUWriteMultipleRegisters():
	#create Write Multiple Registers
	return 1

#print createPDU([3, 0, 0, 0, 1])
