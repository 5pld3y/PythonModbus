import struct
from modbustcp import *
from modbuspdu import *

def ADUReadHoldingRegisters(FunctionCode, StartingAdress, QuantityOfRegisters):
	# Create the full read holding registers ADU
	#print "ADUReadHoldingRegisters FunctionCode: " + str(FunctionCode)
	#print "ADUReadHoldingRegisters StartingAdress: " + str(StartingAdress)
	#print "ADUReadHoldingRegisters QuantityOfRegisters:" + str(QuantityOfRegisters)
	
	TCP = createTCP()
	PDU = createPDU(FunctionCode, StartingAdress, QuantityOfRegisters)
	#print "PDU : " + str(PDU)
	ADU = TCP + PDU
	#print "ADU: " + str(ADU)
	return ADU

def ADUWriteHoldingRegisters():
	# Create the full write holding registers ADU
	return 1

def encode(data):
	# given a list, returns the binary code of the comand.
	return struct.pack('<'+'B'*len(data), *data)

def decode(data):
	# given the binary code, returns a list
	return list(struct.unpack('<'+'B'*len(data), data))

def modbus(FunctionCode = 0, StartingAdress = 0, QuantityOfRegisters = 0, ByteCount = 0, RegisterValue = 0):
	#print "modbus FunctionCode:" + str(FunctionCode)
	#print "modbus StartingAdress:" + str(StartingAdress)
	#print "modbus QuantityOfRegisters:" + str(QuantityOfRegisters) 
	if FunctionCode == 3:
		#print "modbus ADU: " + str(ADUReadHoldingRegisters(FunctionCode, StartingAdress, QuantityOfRegisters))
		return encode(ADUReadHoldingRegisters(FunctionCode, StartingAdress, QuantityOfRegisters))
	elif FunctionCode == 10:
		ADUWriteHoldingRegisters()
	else:
		return "invalid"

def modbus_decode(dataDecoded, Registers):
	ADU = dataDecoded

	# Deals with the TCP
	TCP = ADU[0:7]
	readTCP(TCP)

	# Deals with the PDU
	PDU = ADU[7:]
	ADUandRegistersTuple = readPDU(PDU, Registers)
	

	ADU_response = TCP + ADUandRegistersTuple[0]
	Registers = ADUandRegistersTuple[1]
	return (encode(ADU_response), Registers)

def modbus_response_decode(dataDecoded):
	ADU = dataDecoded

	TCP = ADU[0:7]
	readTCP_silent(TCP)

	PDU = ADU[7:]
	interpretPDU(PDU)
