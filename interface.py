import modbusadu

def MenuClient():
	print ""
	print "== Client Menu =="
	print "[1] Configure Server"
	print "[2] Read"
	print "[3] Write"
	print "[4] Read Loop"
	print "[5] Write Loop"
	print "[6] Quit"
	print ""
	option = raw_input("Select an option: ")
	return option


def MenuClient_Read():
	print ""
	print "== [2] Read =="
	FunctionCode = 3
	StartingAddress = raw_input("Starting Address: ")
	QuantityOfRegisters = raw_input("Quantity of Registers: ")
	request = modbusadu.modbus(FunctionCode, StartingAddress, QuantityOfRegisters)
	return request

