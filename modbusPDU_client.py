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
		return PDUCustomPDU(FunctionCode)


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

## CUSTOM PDU ##

def PDUCustomPDU(FunctionCode):
	PDU = FunctionCode
	return PDU


#####################
## RESPONSE CLIENT ##
#####################

def interpretPDU(PDU):
	FunctionCode = PDU[0]
	if FunctionCode == 3:
		PDUReadHoldingRegisters_interpret(PDU)
	elif FunctionCode == 16:
		PDUWriteMultipleRegisters_interpret(PDU)
	else:
		Error(PDU)


## READ HOLDING REGISTERS ##

def PDUReadHoldingRegisters_interpret(PDU):
	FunctionCode = PDU[0]
	ByteCount = PDU[1]
	RV = PDU[2:]

	print "Number of Registers read: " + str(ByteCount / 2)
	print ""
	printRegisters(RV)

def PDUWriteMultipleRegisters_interpret(PDU):
	FunctionCode = PDU[0]
	SA = PDU[1:3]
	QoR = PDU[4:5]

def Error(PDU):
	FunctionCode = PDU[0]
	ExceptionCode = PDU[1]

	if FunctionCode == 131:
		print "READ HOLDING REGISTERS ERROR!"
	else:
		print "ERROR!"
	print "Function Code: " + str(FunctionCode)
	print "Exception Code: " + str(ExceptionCode)

	if ExceptionCode == 1:
		print "ILLEGAL FUNCTION"
		print "The Function code received in the query is not an allowable action for the server."
		print ""
	elif ExceptionCode == 2:
		print "ILLEGAL DATA ADDRESS"
		print "The data address received in the query is not an allowable address for the server."
		print ""
	elif ExceptionCode == 3:
		print "ILLEGAL DATA VALUE"
		print "A value contained in the query data field is not an allowable value for the serve."
		print ""
	elif ExceptionCode == 4:
		print "SERVER DEVICE FAILURE"
		print "An unrecoverable error occurred while the server was attempting to perform the requested action."
		print ""
	else:
		print "UNKNOW ERROR"
		print "An unknow error occurred."
		print ""
