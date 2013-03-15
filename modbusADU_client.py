# modbusADU_client.py

from modbusTCP_client import *
from modbusPDU_client import *
from binoperations import *


####################
## REQUEST CLIENT ##
####################

def modbus(FunctionCode = 0, StartingAdress = 0, QuantityOfRegisters = 0, ByteCount = 0, RegisterValue = 0):


	PDU = createPDU(FunctionCode, StartingAdress, QuantityOfRegisters, ByteCount, RegisterValue)
	
	Length = len(PDU)
	TransactionIdentifier = 0

	TCP = createTCP(TransactionIdentifier, Length)
	ADU = TCP + PDU

	return encode(ADU)

#####################
## RESPONSE CLIENT ##
#####################

def modbus_response_decode(dataDecoded):
	ADU = dataDecoded

	TCP = ADU[0:7]
	readTCP(TCP)

	PDU = ADU[7:]
	interpretPDU(PDU)
