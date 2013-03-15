# modbusPDU_server.py

from binoperations import *
from registersoperations import *


def decodePDU(PDU, Registers):
	FunctionCode = PDU[0]

	print "== PDU =="
	print "Function Code: " + str(FunctionCode)

	if FunctionCode == 3:
		print "(Read Holding Registers Function)"
		PDU_RESPONSEandRegistersTuple = ReadHoldingRegistersSERVER(PDU, Registers)

		PDU_RESPONSE = [FunctionCode] + PDU_RESPONSEandRegistersTuple[0]
		Registers = PDU_RESPONSEandRegistersTuple[1]
		return (PDU_RESPONSE, Registers)

def ReadHoldingRegistersSERVER(PDU, Registers):
	# Returns a Tuple with the PDU_response and the Registers Values
	FunctionCode = PDU[0]

	SA = PDU[1:3]
	StartingAddress = TwoBytesToInt(SA)
	print "Starting Address: " + str(StartingAddress)

	QoR = PDU[3:5]
	QuantityOfRegisters = TwoBytesToInt(QoR)
	print "Quantity Of Registers: " + str(QuantityOfRegisters)

	# Selects the Values of the Registers to Read
	RVi = Registers[(2*StartingAddress):]
	RV = RVi[:2*QuantityOfRegisters]

	ByteCount = 2 * QuantityOfRegisters
	print "Byte Count: " + str(ByteCount)

	BC = [ByteCount]

	PDU_RESPONSE = BC + RV
	
	print ""
	
	return (PDU_RESPONSE, Registers)