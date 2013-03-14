import sys
import struct
from binoperations import *

def createPDU(FunctionCode, StartingAdress, QuantityOfRegisters):
	# data is a list
	#print "createPDU FunctionCode: " + str(FunctionCode)
	#print "createPDU StartingAdress: " + str(StartingAdress)
	#print "createPDU QuantityOfRegisters: " + str(QuantityOfRegisters)

	if FunctionCode == 3:
		#return "Read"
		#print PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters)
		return PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters)
	elif FunctionCode == 16:
		return "Write"
	else:
		return "Invalid Function Number!"
	#PDU = data
	#return PDU

def readPDU(PDU):
	FunctionCode = PDU[0]

	print "== PDU =="
	print "Function Code: " + str(FunctionCode)

	if FunctionCode == 3:
		print "(Read Holding Registers Function)"
		PDU_response = PDUReadHoldingRegisters_response(PDU)
		PDU_response = [FunctionCode] + PDU_response
		return PDU_response



def PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters):
	#Create Read Holding Registers
	#print "PDUReadHoldingRegisters StartingAdress: " + str(StartingAdress)
	#print "PDUReadHoldingRegisters QuantityOfRegisters: " + str(QuantityOfRegisters)

	FC = [3]
	SA = intTo2Bytes(StartingAdress)
	QoR = intTo2Bytes(QuantityOfRegisters)

	PDU = FC + SA + QoR
	
	#print "PDUReadHoldingRegisters: " + str(PDU)
	
	return PDU

def PDUReadHoldingRegisters_response(PDU):
	FunctionCode = PDU[0]

	SA = PDU[1:3]
	StartingAddress = TwoBytesToInt(SA)
	print "Starting Address: " + str(StartingAddress)

	QoR = PDU[3:5]
	QuantityOfRegisters = TwoBytesToInt(QoR)
	print "Quantity Of Registers: " + str(QuantityOfRegisters)

	## CODIGO PARA ALTERAR REGISTOS

	ByteCount = 2 * QuantityOfRegisters
	print "Byte Count: " + str(ByteCount)

	BC = [ByteCount]
	RV = [0]

	PDU_response = BC + RV
	return PDU_response


def PDUWriteMultipleRegisters():
	#create Write Multiple Registers
	return 1

#print createPDU([3, 0, 0, 0, 1])
