import struct

def intTo2Bytes(value):
	#Receives a int value and converts it to its representation in 2 Bytes in a list

	BYTES = bin(value)[2:].zfill(16)

	MSB = BYTES[0:8]
	LSB = BYTES[8:16]

	MSnumber = int(MSB, 2)
	LSnumber = int(LSB, 2)

	LIST = [MSnumber, LSnumber]
	return LIST

def TwoBytesToInt(listOfBytes):
	#Receives a list of 2 interger represented bytes and returns the corresponding interger.

	BIN = str(bin(listOfBytes[0])[2:].zfill(8)) + str(bin(listOfBytes[1])[2:].zfill(8))
	NUM = int(BIN, 2)

	return NUM

def encode(data):
	# given a list, returns the binary code of the comand.
	return struct.pack('<'+'B'*len(data), *data)

def decode(data):
	# given the binary code, returns a list
	return list(struct.unpack('<'+'B'*len(data), data))
