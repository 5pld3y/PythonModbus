# serverMENU.py

# Imports
from binoperations import *
from fileoperations import *

def initialMENU():
	print ""
	print "== Modbus Server =="
	try:
		PORT = int(raw_input("PORT: "))										# Prompts user for the PORT
	except ValueError:
		print "PORT set to DEFAULT VALUE (502)"
		PORT = 502

	try:
		FirstAddress = int(raw_input("First Address: "))					# Prompts user for the FirstAddress
	except ValueError:
		print "First Address set to DEFAULT VALUE (0)"
		FirstAddress = 0

	try:	
		NumberOfRegisters = int(raw_input("Number Of Registers: "))			# Prompts user for the NumberOfRegisters
	except ValueError:
		print "Number Of Registers set to DEFAULT VALUE (9)"
		NumberOfRegisters = 9

	if (NumberOfRegisters >= 124):
		print "Max value for Number of Registers is 123!"
		print "Number Of Registers: 123"
		NumberOfRegisters = 123

	print ""

	# Creates a Register List with initial value 0 (zero) for all registers.
	Registers = [0] * 2 * NumberOfRegisters

	RegistersANDNumberOfRegistersLIST = RegistersInitializeMENU(Registers, FirstAddress, NumberOfRegisters)
	Registers = RegistersANDNumberOfRegistersLIST[0]
	NumberOfRegisters = RegistersANDNumberOfRegistersLIST[1]

	print ""

	# returns a list to be called MENU_LIST in the server.py file.
	return [PORT, FirstAddress, NumberOfRegisters, Registers]

def RegistersInitializeMENU(Registers, FirstAddress, NumberOfRegisters):
	## REGISTERS INITIALIZATION ROUTINE ##
	# Asks the User to initialize the Registers

	print "Do you want to initialize the Registers?"
	option = raw_input("(type I or i for INITIALIZE, type F or f for READ FROM FILE, ENTER for DEFAULT): ")

	if (option == 'i' or option == 'I'):
		print ""
		print "== Register Initialization =="
		# Calls the function RegistersInitialize to handle the initializations.
		Registers = RegistersInitialize(Registers, FirstAddress, NumberOfRegisters)
		print "Registers: " + str(Registers)
		return [Registers, NumberOfRegisters]

	if (option == 'f' or option == 'F'):
		print ""
		print "== Read Registers from File =="
		filename = raw_input("Filename: ")

		try:
			Registers = readFile(filename)

			print "File Read Sucessful!"

			if (len(Registers) != (2 * NumberOfRegisters)):
				print ""
				print "Number Of Registers actualized!"
				NumberOfRegisters = (len(Registers) / 2)
				print "New Number of Registers: " + str(NumberOfRegisters)
				print ""
				print "Registers: " + str(Registers)
				return [Registers, NumberOfRegisters]
		except IOError:
			print "File not Found!"
			Registers = [0] * 2 * NumberOfRegisters
			print ""
			print "Registers created with default value!"
			print "Registers:" + str(Registers)
			return [Registers, NumberOfRegisters]

	else:
		Registers = [0] * 2 * NumberOfRegisters
		print ""
		print "Registers created with default value!"
		print "Registers:" + str(Registers)
		return [Registers, NumberOfRegisters]

	## END of REGISTERS INITIALIZATION ROUTINE ##


def RegistersInitialize(Registers, FirstAddress, NumberOfRegisters):
	# Function to initalize the registers

	Registers = []			# Creates a empty Registers list.

	i = 0
	while (i < NumberOfRegisters) :
		V = intTo2Bytes(int(raw_input("R" + str(i + FirstAddress) + ": ")))
		Registers = Registers + V
		i += 1

	return Registers 		# Returns the Registers list.



def serverMENU():
	# Prints and returns the user selection.

	print ""
	print "== Server MENU =="
	print "[1] Configure Server"
	print "[2] Listen"
	print "[3] Quit"
	print ""

	option = raw_input("Select an option: ")
	print ""
	return option



