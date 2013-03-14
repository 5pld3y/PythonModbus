from binoperations import *

def createPDU(FunctionCode, StartingAdress, QuantityOfRegisters):

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

def readPDU(PDU, Registers):
	FunctionCode = PDU[0]

	print "== PDU =="
	print "Function Code: " + str(FunctionCode)

	if FunctionCode == 3:
		print "(Read Holding Registers Function)"
		PDUandRegistersTuple = PDUReadHoldingRegisters_response(PDU, Registers)

		PDU_response = [FunctionCode] + PDUandRegistersTuple[0]
		Registers = PDUandRegistersTuple[1]
		return (PDU_response, Registers)

def interpretPDU(PDU):
	FunctionCode = PDU[0]
	if FunctionCode == 3:
		PDUReadHoldingRegisters_interpret(PDU)

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

def PDUReadHoldingRegisters_response(PDU, Registers):
	# Returns a Tuple with the PDU_response and the Registers Values
	FunctionCode = PDU[0]

	SA = PDU[1:3]
	StartingAddress = TwoBytesToInt(SA)
	print "Starting Address: " + str(StartingAddress)

	QoR = PDU[3:5]
	QuantityOfRegisters = TwoBytesToInt(QoR)
	print "Quantity Of Registers: " + str(QuantityOfRegisters)

	RVi = Registers[(2*StartingAddress):]
	RV = RVi[:2*QuantityOfRegisters]

	ByteCount = 2 * QuantityOfRegisters
	print "Byte Count: " + str(ByteCount)

	BC = [ByteCount]

	PDU_response = BC + RV
	print ""
	return (PDU_response, Registers)

def PDUReadHoldingRegisters_interpret(PDU):
	FunctionCode = PDU[0]
	ByteCount = PDU[1]
	RegisterValue = PDU[2:]

	print " == Read Holding Registers =="
	print "Number of Registers: " + str(ByteCount / 2)
	print RegisterValue


def PDUWriteMultipleRegisters():
	#create Write Multiple Registers
	return 1

