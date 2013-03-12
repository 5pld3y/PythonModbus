import sys
import struct

# bytes = [0b00001010]
# print bytes
# print len(bytes)

# encoded = struct.pack('<'+'B'*len(bytes), *bytes)
# decoded = struct.unpack('<'+'B'*len(encoded), encoded)
# print len(encoded)
# print decoded
# print len(decoded)
# print struct.calcsize('<'+'B'*len(bytes))

def createTCP(TransactionIdentifier = [0,0], ProtocolIdentifier = [0,0], Length = [0,1], UnitIdentifier = [0]):

	TI = [0,0]
	PI = [0,0]
	L = [0, 1]
	UI = [0]

	TCP = TI + PI + L + UI
	return TCP




# def IntToByte(binary):
# 	# returns the packed data
# 	data = [binary]
# 	return struct.pack('<'+'B'*len(data), *data)

# print IntToByte(int(0b00001010))

#print createTCP()
#print hex(10)
