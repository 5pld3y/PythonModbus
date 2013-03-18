# modbusADU_client.py

# Imports
from modbusTCP_client import *
from modbusPDU_client import *
from binoperations import *


####################
## REQUEST CLIENT ##
####################

def modbus(TransactionIdentifier, FunctionCode = 0, StartingAdress = 0, QuantityOfRegisters = 0, ByteCount = 0, RegisterValue = 0):
	# function that creates the TCP layer and the PDU layer and returns the encoded ADU request and the Transaction Identifier in a 
	# list.

	# Creation of the PDU.
	PDU = createPDU(FunctionCode, StartingAdress, QuantityOfRegisters, ByteCount, RegisterValue)
	

	# Creation of the TCP
	Length = len(PDU)
	TCPandTransactionIdentifierLIST = createTCP(TransactionIdentifier, Length)		# create TCP returns a list with the TCP
	TCP = TCPandTransactionIdentifierLIST[0]										# and the Transaction Identifier.

	# Gets the Transaction Identifier and joins the TCP and the PDU.
	TransactionIdentifier = TCPandTransactionIdentifierLIST[1]
	ADU = TCP + PDU

	# Returns the encoded (to bytes) ADU and the transaction identifier.
	return [encode(ADU), TransactionIdentifier]

#####################
## RESPONSE CLIENT ##
#####################

def modbus_response_decode(dataDecoded):
	# This function is responsible for interpreting the response ADU.

	ADU = dataDecoded

	# Deals with the TCP.
	TCP = ADU[0:7]
	readTCP(TCP)

	# Deals with the PDU.
	PDU = ADU[7:]
	interpretPDU(PDU)
