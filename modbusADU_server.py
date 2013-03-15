# modbusADU_server.py

from modbusTCP_server import *
from modbusPDU_server import *
from binoperations import *

def modbus_decode(dataDecoded, Registers):
	ADU = dataDecoded

	# Deals with the TCP
	TCP = ADU[0:7]
	decodeTCP(TCP)

	# Deals with the PDU
	PDU = ADU[7:]

	PDU_RESPONSEandRegistersTuple = decodePDU(PDU, Registers)
	

	ADU_RESPONSE = TCP + PDU_RESPONSEandRegistersTuple[0]
	Registers = PDU_RESPONSEandRegistersTuple[1]

	return (encode(ADU_RESPONSE), Registers)
