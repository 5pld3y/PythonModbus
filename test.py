from binoperations import *

Registers = [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6]
#           - 1  -  2  -  3  -  4  -  5  -  6  -

# SA = 2    - 2  -  3  -  4  -  5  -  6  -  7  -

NumberOfRegisters = len(Registers) / 2
#print NumberOfRegisters
StartAddress = 1


def printRegisters(Registers, StartAddress):
	i = 0
	j = StartAddress
	while i < len(Registers):
		X = [Registers[i], Registers[i+1]]
		Num = TwoBytesToInt(X)
		print "R" + str(j) + ": " + str(Num)
		i = i + 2
		j = j + 1


printRegisters(Registers, StartAddress)