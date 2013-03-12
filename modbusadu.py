import sys
import struct
import modbustcp
import modbuspdu

def ADUReadHoldingRegisters():
	# Create the full read holding registers ADU
	TCP = modbustcp.createTCP()
	PDU = modbuspdu.createPDU([3, 0, 0, 0, 1])
	ADU = TCP + PDU
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
	if FunctionCode == 3:
		return encode(ADUReadHoldingRegisters())
	elif FunctionCode == 10:
		ADUWriteHoldingRegisters()
	else:
		return "invalid"

# data = modbus(3)
# print data
# print decode(data)