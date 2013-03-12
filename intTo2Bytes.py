def intTo2Bytes(value):

	BYTES = bin(value)[2:].zfill(16)

	MSB = BYTES[0:8]
	LSB = BYTES[8:16]

	MSnumber = int(LSB, 2)
	LSnumber = int(MSB, 2)

	LIST = [MSnumber, LSnumber]
	return LIST

print intTo2Bytes(255)
