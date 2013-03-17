# serverMENU.py

def initialMENU():
	print ""
	print "== Modbus Server =="
	PORT = int(raw_input("PORT: "))
	FirstAddress = int(raw_input("First Address: "))
	NumberOfRegisters = int(raw_input("Number Of Registers: "))
	print ""

	Registers = [0] * 2 * NumberOfRegisters

	#print Registers

	print "Do you want to initialize the Registers?"
	decision = raw_input("(type Y or y for YES, ENTER for NO) ")

	if (decision == 'y' or decision == 'Y'):
		print ""
		print "== Register Initialization =="
		Registers = RegisterInitialize(Registers, FirstAddress, NumberOfRegisters)
		print "Register: " + str(Registers)

	print ""

	return [PORT, FirstAddress, NumberOfRegisters, Registers]

def RegisterInitialize(Registers, FirstAddress, NumberOfRegisters):

	Registers = []

	i = 0
	while (i < NumberOfRegisters) :
		V = int(raw_input("R" + str(i + FirstAddress) + ": "))
		Registers = Registers + [V]
		i += 1

	return Registers

def serverMENU():
	print ""
	print "== Server MENU =="
	print "[1] Configure Server"
	print "[2] Listen"
	print "[3] Quit"
	print ""

	option = raw_input("Select an option: ")
	print ""
	return option



