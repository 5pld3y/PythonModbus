# clientMENU.py

# Imports
from modbusADU_client import *
from binoperations import *
from clearscreen import *

# Constants
MAX_TIME = 300		# Defines the max Time in ms. (100ms = 1 second)


def InitialMENU():
	# Prints the Initial Menu, and returns a Tuple with the HOST address and PORT number.

	print ""
	print "== Modbus Client =="
	HOST = raw_input("HOST Address: ")

	try:
		PORT = int(raw_input("PORT: "))
	except ValueError:
		print "PORT set to DEFAULT VALUE (502)"
		PORT = 502
		
	print ""
	return (HOST,PORT)



def SucessfulConnection(dataDecoded):
	# Prints the Sucessful Connection message, and gets from the dataDecoded list the First Address and 
	# the Number of Registers. Returns both as a Tuple.

	print ""
	print "Successful connection with server!"
	FirstAddress = dataDecoded[1]
	NumberOfRegisters = dataDecoded[2]
	print "First Address: " + str(FirstAddress)
	print "Number Of Registers: " + str(NumberOfRegisters)
	return (FirstAddress, NumberOfRegisters)



def MenuClient(FirstAddress, NumberOfRegisters, TransactionIdentifier):
	# Prints the Client Menu, and deals with the client selection.
	# This Function can return: 
	# 1. - The already encoded ADU to be sent to the server as a request;
    # 2. - The string "close", that results in the client socket being terminated;
    # 3. - A list with the following syntax: [ "READLOOP", TIME, StartingAddress, QuantityOfRegisters, EncodedData ],
    #      that results in a Read Loop command.
    # 4. - A list with the following syntax: [ "WRITELOOP", TIME, StartingAddress, QuantityOfRegisters, ByteCount ],
    #      that result in a Write Loop command.

	print ""
	print "== Client Menu =="
	print "[1] Read Holding Registers"
	print "[2] Write Multiple Registers"
	print "[3] Enter Custom PDU"
	print "[4] Quit"
	print ""

	option = raw_input("Select an option: ")

	#clearConsole()

	if option == "1":
		# Read Holding Registers
		request = MenuClient_Read(FirstAddress, NumberOfRegisters, TransactionIdentifier)
		return request
	
	elif option == "2":
		# Write Multiple Registers
		request = MenuClient_Write(FirstAddress, NumberOfRegisters, TransactionIdentifier)
		return request

	elif option == "3":
		# Enter Custom PDU
		request = MenuClient_CustomPDU(TransactionIdentifier)
		return request

	elif option == "4":
		# Quit
		print "== [4] Quit =="
		print "Client Closed!"
		return "close"

	else:
		# Invalid Option
		print "Invalid Option! (try again)"


def MenuClient_Read(FirstAddress, NumberOfRegisters, TransactionIdentifier):
	# Function for dealing with a Read Holding Registers request.
	# Can return:
	# 1. - The already encoded ADU to be sent to the server as a request;
    # 3. - A list with the following syntax: [ "READLOOP", TIME, StartingAddress, QuantityOfRegisters, EncodedData ],
    #      that results in a Read Loop command.

	print ""
	print "== [1] Read Holding Registers =="
	FunctionCode = 3 			# Modbus Function Code of a Read Holding Registers Function.
	
	try:
		StartingAddress = int(raw_input("Starting Address: "))
	except ValueError:
		print "Value Error! (try again)"
		return None

	# Checks if Starting Address is a valid number, doing tests with the First Address and the Number of Registers of the Server.
	# If it is not, returns None and breaks.
	if (StartingAddress < FirstAddress):
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		return None
	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		return None

	try:
		QuantityOfRegisters = int(raw_input("Quantity of Registers: "))
	except ValueError:
		print "Value Error! (try again)"
		return None

	# Checks if Quantity of Registers is a valid number, doing tests with the First Address and the Number of Registers of the Server.
	# If it is not, returns None and breaks.
	if ((QuantityOfRegisters+StartingAddress) > (FirstAddress + NumberOfRegisters)):
		print "Too much Registers! Must be less or equal to " + str(FirstAddress+NumberOfRegisters-StartingAddress)
		return None
	if ((QuantityOfRegisters) >= 124):
		print "Too much Registers! Must be less than 124!"
		return None

	# Check to see if a user wants a loop or not.
	try:
		Time = int(raw_input(("Time in ms (press ENTER for just one read): ")))
	except ValueError:
		# If not, returns Time = None
		Time = None

	# If a user wans a loop...
	if Time != None:
		# Tests if Time is a correct value.
		if Time < 0:
			print "Time must be positive!"
		elif Time > MAX_TIME:
			print "Time mus be less than " + str(MAX_TIME) + "ms"
		else:
			# If it is, calls the modbus function, to construct the  request ADU.
			request = modbus(TransactionIdentifier, FunctionCode, StartingAddress, QuantityOfRegisters)

			#returns a list, with the first parameter "READLOOP", to be identified in the client program.
			return ["READLOOP", Time, StartingAddress, QuantityOfRegisters, request[0]]

	# If it's not a loop, calls the modbus function, to construct the request ADU, and returns the already encoded data.
	request = modbus(TransactionIdentifier, FunctionCode, StartingAddress, QuantityOfRegisters)
	return request


def MenuClient_Write(FirstAddress, NumberOfRegisters, TransactionIdentifier):
	# Function for dealing with a Write Multiple Registers request.
	# Can return:
	# 1. - The already encoded ADU to be sent to the server as a request;
    # 4. - A list with the following syntax: [ "WRITELOOP", TIME, StartingAddress, QuantityOfRegisters, ByteCount ],
    #      that result in a Write Loop command.

	print ""
	print "== [2] Write Multiple Registers =="
	
	FunctionCode = 16					# Modbus Function Code of a Write Multiple Registers Function.
	
	try:
		StartingAddress = int(raw_input("Starting Address: "))
	except ValueError:
		print "Value Error! (try again)"

	# Checks if Starting Address is a valid number, doing tests with the First Address and the Number of Registers of the Server.
	# If it is not, returns None and breaks. 
	if (StartingAddress < FirstAddress):
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		return None
	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		return None

	try:
		QuantityOfRegisters = int(raw_input("Quantity Of Registers: "))
	except ValueError:
		print "Value Error! (try again)"
		return None

	# Checks if Quantity of Registers is a valid number, doing tests with the First Address and the Number of Registers of the Server.
	# If it is not, returns None and breaks.
	if ((QuantityOfRegisters+StartingAddress) > (FirstAddress + NumberOfRegisters)):
		print "Too much Registers! Must be less or equal to " + str(FirstAddress+NumberOfRegisters-StartingAddress)
		return None
	if (QuantityOfRegisters >= 124):
		print "Too much Registers! Must be less than 124!"
		return None

	ByteCount = 2 * QuantityOfRegisters


	# Check to see if a user wants a loop or not.
	try:
		Time = int(raw_input(("Time in ms (press ENTER for just one read): ")))
	except ValueError:
		Time = None 				# If not, returns Time = None

	# If a user wans a loop...
	if Time != None:
		# Tests if Time is a correct value.
		if Time < 0:
			print "Time must be positive!"
		elif Time > MAX_TIME:
			print "Time mus be less than " + str(MAX_TIME) + "ms"
		else:
			# if it is, returns a list, with the first parameter "WRITELOOP", to be identified in the client program.
			return ["WRITELOOP", Time, StartingAddress, QuantityOfRegisters, ByteCount]


	# Write to Registers Routine #

	RegisterValue = []
	i = QuantityOfRegisters
	j = StartingAddress

	while i>0:
		try:
			X = intTo2Bytes(int(raw_input("R" + str(j) + ": ")))
		except ValueError:
			print "Value Error! try again!"
			return None
		RegisterValue = RegisterValue + X
		i = i - 1
		j = j + 1

	# End of Write to Registers Routine #

	# If it's not a loop, calls the modbus function, to construct the request ADU, and returns the already encoded data.
	request = modbus(TransactionIdentifier, FunctionCode, StartingAddress, QuantityOfRegisters, ByteCount, RegisterValue)
	return request

def MenuClient_CustomPDU(TransactionIdentifier):
	# Function to generate a custom (user inputed) PDU.
	# FunctionCode passed as the full PDU.

	print ""
	print "== [3] Custom PDU =="
	print ""
	print "Insert each byte of the PDU in a decimal representation, separated by spaces"
	INPUT = raw_input("Enter the PDU in int with spaces: ")

	# Converts the input to a list
	FunctionCode = map(int, INPUT.split())
	print "PDU: " + str(FunctionCode)
	print ""

	# Calls the modbus function, to construct the ADU and encode the messagem.
	request = modbus(TransactionIdentifier, FunctionCode)
	return request