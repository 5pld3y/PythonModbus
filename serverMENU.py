# serverMENU.py

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
	option = raw_input("(type Y or y for YES, ENTER for NO) ")

	if (option == 'y' or option == 'Y'):
		print ""
		print "== Register Initialization =="
		# Calls the function RegistersInitialize to handle the initializations.
		Registers = RegistersInitialize(Registers, FirstAddress, NumberOfRegisters)
		print "Register: " + str(Registers)

	## END of REGISTERS INITIALIZATION ROUTINE ##

	print ""

	# returns a list to be called MENU_LIST in the server.py file.
	return [PORT, FirstAddress, NumberOfRegisters, Registers]



def RegistersInitialize(Registers, FirstAddress, NumberOfRegisters):
	# Function to initalize the registers

	Registers = []			# Creates a empty Registers list.

	i = 0
	while (i < NumberOfRegisters) :
		V = int(raw_input("R" + str(i + FirstAddress) + ": "))
		Registers = Registers + [V]
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



