from modbusADU_client import *
from binoperations import *

def SucessfulConnection(dataDecoded):
	print ""
	print "Successful connection with server!"
	FirstAddress = dataDecoded[1]
	NumberOfRegisters = dataDecoded[2]
	print "First Address: " + str(FirstAddress)
	print "Number Of Registers: " + str(NumberOfRegisters)
	return [FirstAddress, NumberOfRegisters]


def MenuClient(FirstAddress, NumberOfRegisters):
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

	if option == "2":
		request = MenuClient_Read(FirstAddress, NumberOfRegisters)
		return request
	elif option == "3":
		request = MenuClient_Write(FirstAddress, NumberOfRegisters)
		return request
	elif option == "4":
		print "Option 4"
		return None
	elif option == "5":
		print "Option 5"
		return None
	elif option == "6":
		print "== [6] Quit =="
		print "Client Closed!"
		return "close"
	else:
		print "Invalid Option! (try again)"


def MenuClient_Read(FirstAddress, NumberOfRegisters):
	print ""
	print "== [2] Read Holding Registers =="
	FunctionCode = 3
	
	StartingAddress = int(raw_input("Starting Address: "))
	if (StartingAddress < FirstAddress):
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		return None
	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		return None


	QuantityOfRegisters = int(raw_input("Quantity of Registers: "))
	if ((QuantityOfRegisters+StartingAddress) > (FirstAddress + NumberOfRegisters)):
		print "Too much Registers! Must be less or equal to " + str(FirstAddress+NumberOfRegisters-StartingAddress)
		return None

	request = modbus(FunctionCode, StartingAddress, QuantityOfRegisters)
	return request


def MenuClient_Write(FirstAddress, NumberOfRegisters):
	print ""
	print "== [3] Write Multiple Registers =="
	
	FunctionCode = 16
	
	StartingAddress = int(raw_input("Starting Address: "))
	if (StartingAddress < FirstAddress):
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		return None
	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		return None

	QuantityOfRegisters = int(raw_input("Quantity Of Registers: "))
	if ((QuantityOfRegisters+StartingAddress) > (FirstAddress + NumberOfRegisters)):
		print "Too much Registers! Must be less or equal to " + str(FirstAddress+NumberOfRegisters-StartingAddress)
		return None

	ByteCount = 2 * QuantityOfRegisters

	RegisterValue = []
	i = QuantityOfRegisters
	j = StartingAddress

	while i>0:
		X = intTo2Bytes(int(raw_input("R" + str(j) + ": ")))
		RegisterValue = RegisterValue + X
		i = i - 1
		j = j + 1

	request = modbus(FunctionCode, StartingAddress, QuantityOfRegisters, ByteCount, RegisterValue)
	return request