# modbusPDU_server.py

from binoperations import *
from registersoperations import *


def decodePDU(PDU, Registers, FirstAddress, NumberOfRegisters):
	FunctionCode = PDU[0]

	print "== PDU =="
	print "Function Code: " + str(FunctionCode)

	if FunctionCode == 3:
		print "(Read Holding Registers Function)"
		PDU_RESPONSEandRegistersTuple = ReadHoldingRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters)

		PDU_RESPONSE = PDU_RESPONSEandRegistersTuple[0]
		Registers = PDU_RESPONSEandRegistersTuple[1]
		return (PDU_RESPONSE, Registers)

	if FunctionCode == 16:
		print "(Write Multiple Registers Function)"
		PDU_RESPONSEandRegistersTuple = WriteMultipleRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters)

		PDU_RESPONSE = PDU_RESPONSEandRegistersTuple[0]
		Registers = PDU_RESPONSEandRegistersTuple[1]
		return (PDU_RESPONSE, Registers)

	else:
		FC = [FunctionCode]
		ExceptionCode = 1
		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		EC = [ExceptionCode]
		print "EXCEPTION: ILLEGAL FUNCTION!"
		print "The function code received in the query is not an allowable action for the server"
		PDU_RESPONSE = FC + EC
		return (PDU_RESPONSE, Registers)


def ReadHoldingRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters):
	# Returns a Tuple with the PDU_response and the Registers Values
	FunctionCode = PDU[0]
	FC = [FunctionCode]

	SA = PDU[1:3]
	StartingAddress = TwoBytesToInt(SA)

	if (len(PDU) != 5):
		ExceptionCode = 4
		EC = [ExceptionCode]
		FunctionCode = 131 #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC
		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: SERVER DEVICE FAILURE!"
		print "An unrecoverable error occurred while the server was attempting to perform the requested action."
		print ""
		return (PDU_RESPONSE, Registers)

	print "Starting Address: " + str(StartingAddress)
	if (StartingAddress < FirstAddress):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 131  #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		print ""
		return (PDU_RESPONSE, Registers)

	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 131  #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		print ""
		return (PDU_RESPONSE, Registers)

	QoR = PDU[3:5]
	QuantityOfRegisters = TwoBytesToInt(QoR)
	print "Quantity Of Registers: " + str(QuantityOfRegisters)

	if ((QuantityOfRegisters+StartingAddress) > (FirstAddress + NumberOfRegisters)):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 131  #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Too much Registers! Must be less or equal to " + str(FirstAddress+NumberOfRegisters-StartingAddress)
		return (PDU_RESPONSE, Registers)
	

	# Selects the Values of the Registers to Read
	RVi = Registers[(2*(StartingAddress-FirstAddress)):]
	RV = RVi[:2*QuantityOfRegisters]

	ByteCount = 2 * QuantityOfRegisters
	print "Byte Count: " + str(ByteCount)

	BC = [ByteCount]

	PDU_RESPONSE = FC + BC + RV
	
	print ""
	
	return (PDU_RESPONSE, Registers)


def WriteMultipleRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters):
	FunctionCode = PDU[0]
	FC = [FunctionCode]

	SA = PDU[1:3]
	StartingAddress = TwoBytesToInt(SA)
	print "Starting Address: " + str(StartingAddress)

	if (StartingAddress < FirstAddress):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 144  #0x90
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		print ""
		return (PDU_RESPONSE, Registers)

	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 144  #0x90
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		print ""
		return (PDU_RESPONSE, Registers)

	
	QoR = PDU[3:5]
	QuantityOfRegisters = TwoBytesToInt(QoR)
	print "Quantity Of Registers: " + str(QuantityOfRegisters)
	
	ByteCount = PDU[5]
	print "Byte Count: " + str(ByteCount)
	
	RegisterValue = PDU[6:]
	print "Register Value: " + str(RegisterValue)
	
	i = (StartingAddress-FirstAddress)*2
	k = 0

	while (k < QuantityOfRegisters*2):
		Registers[i] = RegisterValue[k]
		i = i + 1
		k = k + 1

	print "Register: " + str(Registers)
	print ""

	PDU_RESPONSE = FC + SA + QoR

	return (PDU_RESPONSE, Registers)

