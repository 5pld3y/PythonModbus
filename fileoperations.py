# fileoperations.py

# Imports
from binoperations import *
import os

registers = [0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7]

def writeFile(Registers, filename):
	i = 0
	j = 0
 	stringRegisters = ""
 	length = len(Registers)
 	while i < length:
 		X = [Registers[i], Registers[i+1]]
 		Num = TwoBytesToInt(X)
 		stringRegisters = stringRegisters + str(Num) + "\r\r\n"
 		i = i + 2
 		j = j + 1
 	
	f = open(filename,'w+')
	f.write(stringRegisters) 
	f.close()


def readFile(filename, NumberOfRegisters):
	f = open(filename, 'r+')
	try:
		lines = [int(line.strip()) for line in f]
	except ValueError:
		print "Error reading!"
		registers = [0] * 2 * NumberOfRegisters
		print "Registers set to DEFAULT VALUE!"
		print "Registers: " + str(registers)
		print ""
		f.close()
		return registers
	f.close()
	
	length = len(lines)
	registers = []
	i = 0
	while i < length:
		X = intTo2Bytes(lines[i])
		registers = registers + X
		i += 1

	return registers
