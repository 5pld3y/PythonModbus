import sys
import struct
import intTo2Bytes

def createPDU(FunctionCode, StartingAdress, QuantityOfRegisters):
	# data is a list
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

def PDUReadHoldingRegisters(StartingAdress, QuantityOfRegisters):
	#Create Read Holding Registers
	#print "PDUReadHoldingRegisters StartingAdress: " + str(StartingAdress)
	#print "PDUReadHoldingRegisters QuantityOfRegisters: " + str(QuantityOfRegisters)

	FC = [3]
	SA = intTo2Bytes.intTo2Bytes(StartingAdress)
	QoR = intTo2Bytes.intTo2Bytes(QuantityOfRegisters)

	PDU = FC + SA + QoR
	
	#print "PDUReadHoldingRegisters: " + str(PDU)
	
	return PDU

def PDUWriteMultipleRegisters():
	#create Write Multiple Registers
	return 1

#print createPDU([3, 0, 0, 0, 1])
