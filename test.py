from binoperations import *

# Registers = [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6]
# #           - 1  -  2  -  3  -  4  -  5  -  6  -

# # SA = 2    - 2  -  3  -  4  -  5  -  6  -  7  -

# NumberOfRegisters = len(Registers) / 2
# #print NumberOfRegisters
# StartAddress = 1


# def printRegisters(Registers, StartAddress):
# 	i = 0
# 	j = StartAddress
# 	while i < len(Registers):
# 		X = [Registers[i], Registers[i+1]]
# 		Num = TwoBytesToInt(X)
# 		print "R" + str(j) + ": " + str(Num)
# 		i = i + 2
# 		j = j + 1


# printRegisters(Registers, StartAddress)


# def ReadHoldingRegistersSERVER(PDU, Registers):
# 	# Returns a Tuple with the PDU_response and the Registers Values
# 	FunctionCode = PDU[0]

# 	SA = PDU[1:3]
# 	StartingAddress = TwoBytesToInt(SA)
# 	print "Starting Address: " + str(StartingAddress)

# 	QoR = PDU[3:5]
# 	QuantityOfRegisters = TwoBytesToInt(QoR)
# 	print "Quantity Of Registers: " + str(QuantityOfRegisters)

# 	# Selects the Values of the Registers to Read
# 	RVi = Registers[(2*StartingAddress):]
# 	RV = RVi[:2*QuantityOfRegisters]

# 	ByteCount = 2 * QuantityOfRegisters
# 	print "Byte Count: " + str(ByteCount)

# 	BC = [ByteCount]

# 	PDU_RESPONSE = BC + RV
	
# 	print ""
	
# 	return (PDU_RESPONSE, Registers)


PDU = [16 , 0, 0, 0, 4, 8, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5]
##     0    1  2  3  4  5   6  7  8  9 10 11 12 13 14 15


Register = [20, 20, 19, 19, 18, 18, 17, 17, 16, 16, 15, 15, 14, 14, 13, 13, 12, 12, 11, 11]
##           0  1    2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
##             0  -   1   -   2    -  3    -  4    -  5   -  6    -   7    -  8    -  9


FunctionCode = PDU[0]

SA = PDU[1:3]
StartingAddress = TwoBytesToInt(SA)
print "Starting Address: " + str(StartingAddress)

QoR = PDU[3:5]
QuantityOfRegisters = TwoBytesToInt(QoR)
print "Quantity Of Registers: " + str(QuantityOfRegisters)

ByteCount = PDU[5]
print "Byte Count: " + str(ByteCount)

RegisterValue = PDU[6:]
print "Register Value: " + str(RegisterValue)

StartingAddress = 3
QuantityOfRegisters = 5

i = StartingAddress*2
k = 0

while (k < QuantityOfRegisters*2):
	Register[i] = RegisterValue[k]
	i = i + 1
	k = k + 1

print Register
