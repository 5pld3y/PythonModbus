# modbusPDU_client.py

from binoperations import *
from registersoperations import *

####################
## REQUEST CLIENT ##
####################

def createPDU(FunctionCode=0, StartingAdress=0, QuantityOfRegisters=0, ByteCount=0, RegisterValue=0):

	if FunctionCode == 3:
		return PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters)

	elif FunctionCode == 16:
		return PDUWriteMultipleRegisters_CREATE(StartingAdress, QuantityOfRegisters, ByteCount, RegisterValue)

	else:
		return "Invalid Function Number!"


## READ HOLDING REGISTERS ##

def PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters):
	#Create Read Holding Registers

	FC = [3]
	SA = intTo2Bytes(StartingAdress)
	QoR = intTo2Bytes(QuantityOfRegisters)

	PDU = FC + SA + QoR
	
	return PDU

## WRITE MULTIPLE REGISTERS ##

def PDUWriteMultipleRegisters_CREATE(StartingAdress, QuantityOfRegisters, ByteCount, RegisterValue):
	FC = [16]
	SA = intTo2Bytes(StartingAdress)
	QoR = intTo2Bytes(QuantityOfRegisters)
	BC = [ByteCount]
	RV = RegisterValue

	PDU = FC + SA + QoR + BC + RV

	return PDU


#####################
## RESPONSE CLIENT ##
#####################

def interpretPDU(PDU):
	FunctionCode = PDU[0]
	if FunctionCode == 3:
		PDUReadHoldingRegisters_interpret(PDU)

## READ HOLDING REGISTERS ##

def PDUReadHoldingRegisters_interpret(PDU):
	FunctionCode = PDU[0]
	ByteCount = PDU[1]
	RegisterValue = PDU[2:]

	print "Number of Registers read: " + str(ByteCount / 2)
	print ""
	printRegisters(RegisterValue)