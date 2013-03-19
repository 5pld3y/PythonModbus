# serverMENU.py

# Imports
from binoperations import *
from fileoperations import *

def initialMENU():
	print ""
	print "== Modbus Server =="
	PORT = int(raw_input("PORT: "))										# Prompts user for the PORT
	FirstAddress = int(raw_input("First Address: "))					# Prompts user for the FirstAddress
	NumberOfRegisters = int(raw_input("Number Of Registers: "))			# Prompts user for the NumberOfRegisters
	print ""

	# Creates a Register List with initial value 0 (zero) for all registers.
	Registers = [0] * 2 * NumberOfRegisters



	## REGISTERS INITIALIZATION ROUTINE ##
	# Asks the User to initialize the Registers

	print "Do you want to initialize the Registers?"
	option = raw_input("(type I or i for INITIALIZE, type F or f for READ FROM FILE, ENTER for NO): ")

	if (option == 'i' or option == 'I'):
		print ""
		print "== Register Initialization =="
		# Calls the function RegistersInitialize to handle the initializations.
		Registers = RegistersInitialize(Registers, FirstAddress, NumberOfRegisters)
		print "Registers: " + str(Registers)

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
		except IOError:
			print "File not Found!"
			Registers = [0] * 2 * NumberOfRegisters
			print ""
			print "Registers created with default value!"
			print "Registers:" + str(Registers)




	## END of REGISTERS INITIALIZATION ROUTINE ##

	print ""

	# returns a list to be called MENU_LIST in the server.py file.
	return [PORT, FirstAddress, NumberOfRegisters, Registers]



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



