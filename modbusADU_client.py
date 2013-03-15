# modbusADU_client.py

from modbusTCP_client import *
from modbusPDU_client import *
from binoperations import *


####################
## REQUEST CLIENT ##
####################

def modbus(TransactionIdentifier, FunctionCode = 0, StartingAdress = 0, QuantityOfRegisters = 0, ByteCount = 0, RegisterValue = 0):


	PDU = createPDU(FunctionCode, StartingAdress, QuantityOfRegisters, ByteCount, RegisterValue)
	
	Length = len(PDU)

	TCPandTransactionIdentifierLIST = createTCP(TransactionIdentifier, Length)
	TCP = TCPandTransactionIdentifierLIST[0]
	TransactionIdentifier = TCPandTransactionIdentifierLIST[1]
	ADU = TCP + PDU

	return [encode(ADU), TransactionIdentifier]

#####################
## RESPONSE CLIENT ##
#####################

def modbus_response_decode(dataDecoded):
	ADU = dataDecoded

	TCP = ADU[0:7]
	readTCP(TCP)

	PDU = ADU[7:]
	interpretPDU(PDU)
