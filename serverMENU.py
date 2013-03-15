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
	decision = raw_input("(type Y for Yes) ")

	if (decision == 'y' or decision == 'Y'):
	    print "Register Initialization"

	print ""

	return [PORT, FirstAddress, NumberOfRegisters, Registers]

