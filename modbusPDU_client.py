# modbusPDU_client.py

from binoperations import *
from registersoperations import *

####################
## REQUEST CLIENT ##
####################

def createPDU(FunctionCode=0, StartingAdress=0, QuantityOfRegisters=0, ByteCount=0, RegisterValue=0):
	# This function is used to create the PDU for the request. Returns the PDU.

	if FunctionCode == 3:
		# Read Holding Registers
		return PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters)

	elif FunctionCode == 16:
		# Write Multiple Registers
		return PDUWriteMultipleRegisters_CREATE(StartingAdress, QuantityOfRegisters, ByteCount, RegisterValue)

	else:
		# Custom Fuction
		return PDUCustomPDU(FunctionCode)


## READ HOLDING REGISTERS ##

def PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters):
	#Create Read Holding Registers PDU

	FC = [3]

	# The intTo2Bytes function is called to convert a single int value to a list of two bytes, each represented as 
	# an int value.
	SA = intTo2Bytes(StartingAdress)
	QoR = intTo2Bytes(QuantityOfRegisters)

	PDU = FC + SA + QoR
	
	return PDU

## WRITE MULTIPLE REGISTERS ##

def PDUWriteMultipleRegisters_CREATE(StartingAdress, QuantityOfRegisters, ByteCount, RegisterValue):
	# Create Write Multiple Registers PDU

	FC = [16]

	# The intTo2Bytes function is called to convert a single int value to a list of two bytes, each represented as 
	# an int value.
	SA = intTo2Bytes(StartingAdress)
	QoR = intTo2Bytes(QuantityOfRegisters)

	BC = [ByteCount]
	RV = RegisterValue

	PDU = FC + SA + QoR + BC + RV

	return PDU

## CUSTOM PDU ##

def PDUCustomPDU(FunctionCode):
	# Creates a custom PDU from "FunctionCode"

	PDU = FunctionCode
	return PDU


#####################
## RESPONSE CLIENT ##
#####################

def interpretPDU(PDU):
	# Interprets the response PDU.

	FunctionCode = PDU[0]

	if FunctionCode == 3:
		# Read Holding Registers
		PDUReadHoldingRegisters_interpret(PDU)

	elif FunctionCode == 16:
		# Write Multiple Registers
		PDUWriteMultipleRegisters_interpret(PDU)
	else:
		# Error!
		Error(PDU)


## READ HOLDING REGISTERS ##

def PDUReadHoldingRegisters_interpret(PDU):
	# Read Holding Registers

	FunctionCode = PDU[0]
	ByteCount = PDU[1]
	RV = PDU[2:]

	print "Number of Registers read: " + str(ByteCount / 2)
	print ""

	# Function that prints the registers.
	printRegisters(RV)


## WRITE MULTIPLE REGISTERS ##

def PDUWriteMultipleRegisters_interpret(PDU):
	# Write Multipe Registers

	FunctionCode = PDU[0]
	SA = PDU[1:3]
	QoR = PDU[4:5]


## ERROR! ##

def Error(PDU):
	## Gets the Function Code (error) and the Exception Code and prints them.

	FunctionCode = PDU[0]
	ExceptionCode = PDU[1]

	if FunctionCode == 131:
		print "READ HOLDING REGISTERS ERROR!"
	elif FunctionCode == 144:
		print "WRITE MULTIPLE REGISTERS ERROR!"
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
