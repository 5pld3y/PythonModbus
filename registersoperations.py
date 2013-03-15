from binoperations import *

def printRegisters(Registers, StartAddress=0):
	i = 0
	j = StartAddress
	while i < len(Registers):
		X = [Registers[i], Registers[i+1]]
		Num = TwoBytesToInt(X)
		print "R" + str(j) + ": " + str(Num)
		i = i + 2
		j = j + 1
