from modbusADU_client import *
from binoperations import *

MAX_TIME = 300

def InitialMENU():
	print ""
	print "== Modbus Client =="
	HOST = raw_input("HOST Address: ")
	PORT = int(raw_input("PORT: "))
	print ""
	return (HOST,PORT)

def SucessfulConnection(dataDecoded):
	print ""
	print "Successful connection with server!"
	FirstAddress = dataDecoded[1]
	NumberOfRegisters = dataDecoded[2]
	print "First Address: " + str(FirstAddress)
	print "Number Of Registers: " + str(NumberOfRegisters)
	return (FirstAddress, NumberOfRegisters)


def MenuClient(FirstAddress, NumberOfRegisters, TransactionIdentifier):
	print ""
	print "== Client Menu =="
	print "[1] Configure Server"
	print "[2] Read Holding Registers"
	print "[3] Write Multiple Registers"
	print "[4] Enter Custom PDU"
	print "[5] Quit"
	print ""

	option = raw_input("Select an option: ")

	if option == "2":
		request = MenuClient_Read(FirstAddress, NumberOfRegisters, TransactionIdentifier)
		return request
	elif option == "3":
		request = MenuClient_Write(FirstAddress, NumberOfRegisters, TransactionIdentifier)
		return request
	elif option == "4":
		request = MenuClient_CustomPDU(TransactionIdentifier)
		return request
	elif option == "5":
		print "== [5] Quit =="
		print "Client Closed!"
		return "close"
	else:
		print "Invalid Option! (try again)"


def MenuClient_Read(FirstAddress, NumberOfRegisters, TransactionIdentifier):
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

	try:
		Time = int(raw_input(("Time in ms (press ENTER for just one read): ")))
	except ValueError:
		Time = None

	if Time != None:
		if Time < 0:
			print "Time must be positive!"
		elif Time > MAX_TIME:
			print "Time mus be less than " + str(MAX_TIME) + "ms"
		else:
			request = modbus(TransactionIdentifier, FunctionCode, StartingAddress, QuantityOfRegisters)
			return ["READLOOP", Time, StartingAddress, QuantityOfRegisters, request[0]]

	request = modbus(TransactionIdentifier, FunctionCode, StartingAddress, QuantityOfRegisters)
	return request


def MenuClient_Write(FirstAddress, NumberOfRegisters, TransactionIdentifier):
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

	request = modbus(TransactionIdentifier, FunctionCode, StartingAddress, QuantityOfRegisters, ByteCount, RegisterValue)
	return request

def MenuClient_CustomPDU(TransactionIdentifier):
	# FunctionCode passed as the full PDU.

	INPUT = raw_input("Enter the PDU in int with spaces: ")
	#FunctionCode = list(LIST)
	FunctionCode = map(int, INPUT.split())
	print "PDU: " + str(FunctionCode)
	print ""

	request = modbus(TransactionIdentifier, FunctionCode)
	return request