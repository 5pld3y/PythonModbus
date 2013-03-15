from modbusADU_client import *

def MenuClient():
	print ""
	print "== Client Menu =="
	print "[1] Configure Server"
	print "[2] Read Holding Registers"
	print "[3] Write Multiple Registers"
	print "[4] Read Loop"
	print "[5] Write Loop"
	print "[6] Quit"
	print ""
	option = raw_input("Select an option: ")
	return option


def MenuClient_Read(FirstAddress, NumberOfRegisters):
	print ""
	print "== [2] Read Holding Registers =="
	FunctionCode = 3
	
	StartingAddress = int(raw_input("Starting Address: "))
	if (StartingAddress < FirstAddress):
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		return None
		# Fazer funcao para acabar de detetar o erro

	QuantityOfRegisters = int(raw_input("Quantity of Registers: "))
	#print "MenuClient_Read" + " " + str(StartingAddress) + " " + str(QuantityOfRegisters)
	#print "StartingAddress: " + str(StartingAddress)
	#print "QuantityOfRegisters: " + str(QuantityOfRegisters)
	request = modbus(FunctionCode, StartingAddress, QuantityOfRegisters)
	return request

