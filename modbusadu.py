import sys
import struct
import modbustcp
import modbuspdu

def ADUReadHoldingRegisters(FunctionCode, StartingAdress, QuantityOfRegisters):
	# Create the full read holding registers ADU
	#print "ADUReadHoldingRegisters FunctionCode: " + str(FunctionCode)
	#print "ADUReadHoldingRegisters StartingAdress: " + str(StartingAdress)
	#print "ADUReadHoldingRegisters QuantityOfRegisters:" + str(QuantityOfRegisters)
	
	TCP = modbustcp.createTCP()
	PDU = modbuspdu.createPDU(FunctionCode, StartingAdress, QuantityOfRegisters)
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

# data = modbus(3)
# print data
# print decode(data)