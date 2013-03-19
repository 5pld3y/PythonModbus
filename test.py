def RegistersInitialize(Registers, FirstAddress, NumberOfRegisters):
	# Function to initalize the registers

	Registers = []			# Creates a empty Registers list.

	i = 0
	while (i < NumberOfRegisters) :
		V = intTo2Bytes(int(raw_input("R" + str(i + FirstAddress) + ": ")))
		Registers = Registers + [V]
		i += 1

	return Registers 		# Returns the Registers list.


	# Write to Registers Routine #

	RegisterValue = []
	i = QuantityOfRegisters
	j = StartingAddress

	while i>0:
		X = intTo2Bytes(int(raw_input("R" + str(j) + ": ")))
		RegisterValue = RegisterValue + X
		i = i - 1
		j = j + 1

	# End of Write to Registers Routine #