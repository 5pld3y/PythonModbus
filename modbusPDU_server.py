# modbusPDU_server.py

# Imports
from binoperations import *
from registersoperations import *



def decodePDU(PDU, Registers, FirstAddress, NumberOfRegisters):
	# Function used to decode the PDU and, if requested, to actualize the values of the Registers list.

	FunctionCode = PDU[0]

	print "== PDU =="
	print "Function Code: " + str(FunctionCode)

	# READ HOLDING REGISTERS
	if FunctionCode == 3:
		print "(Read Holding Registers Function)"

		# Calls the function to deal with a Read Holding Registers request, and returns a tuple with the PDU to be 
		# used as a response and the new values of the Registers list.
		PDU_RESPONSEandRegistersTuple = ReadHoldingRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters)

		PDU_RESPONSE = PDU_RESPONSEandRegistersTuple[0]
		Registers = PDU_RESPONSEandRegistersTuple[1]
		return (PDU_RESPONSE, Registers)

	# WRITE MULTIPLE REGISTERS
	if FunctionCode == 16:
		print "(Write Multiple Registers Function)"

		# Calls a function to deal with a Write Multiple Registers request, and returns a tuple with the PDU to be
		# used as a response and the new values of the Registers list.
		PDU_RESPONSEandRegistersTuple = WriteMultipleRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters)

		PDU_RESPONSE = PDU_RESPONSEandRegistersTuple[0]
		Registers = PDU_RESPONSEandRegistersTuple[1]
		return (PDU_RESPONSE, Registers)

	# ERRORS
	else:
		# If it is not a Read Holding Registers or a Write Multiple Registers function, generates an exception with 
		# code 1. Prints this information to the console and returns a tuple with the PDU response, 
		# (Function Code followed by the Exception Code) and the Registers list.

		FC = [FunctionCode]
		ExceptionCode = 1
		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		EC = [ExceptionCode]
		print "EXCEPTION: ILLEGAL FUNCTION!"
		print "The function code received in the query is not an allowable action for the server"
		PDU_RESPONSE = FC + EC
		return (PDU_RESPONSE, Registers)



## READ HOLDING REGISTERS ##

def ReadHoldingRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters):
	# Returns a Tuple with the PDU_response and the Registers Values.
	# If sucessful, returns the value of the registers read.
	# If not sucessful, returns Function Code 131 (0x83) and the corresponding Exception Code.

	FunctionCode = PDU[0]
	FC = [FunctionCode]

	SA = PDU[1:3]
	StartingAddress = TwoBytesToInt(SA)

	# Tests for the Illegal Data Value. If it's different from 5 bytes, generates Exception Code 3.
	if (len(PDU) != 5):
		ExceptionCode = 3
		EC = [ExceptionCode]
		FunctionCode = 131 #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA VALUE!"
		print "A value contained in the query data field is not an allowable value for the serve."
		print ""
		return (PDU_RESPONSE, Registers)

	print "Starting Address: " + str(StartingAddress)
	
	# Tests for illegal values for the Starting Address. Returns Exception Code 2 if founds an error.
	if (StartingAddress < FirstAddress):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 131  #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		print ""
		return (PDU_RESPONSE, Registers)

	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 131  #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		print ""
		return (PDU_RESPONSE, Registers)

	QoR = PDU[3:5]
	QuantityOfRegisters = TwoBytesToInt(QoR)
	print "Quantity Of Registers: " + str(QuantityOfRegisters)

	# Tests for illegal values of Quantity of Registers. If and error is found, generates Exception Code 2.
	if ((QuantityOfRegisters+StartingAddress) > (FirstAddress + NumberOfRegisters)):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 131  #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Too much Registers! Must be less or equal to " + str(FirstAddress+NumberOfRegisters-StartingAddress)
		return (PDU_RESPONSE, Registers)
	

	# If no error is found....

	# Selects the Values of the Registers to Read
	RVi = Registers[(2*(StartingAddress-FirstAddress)):]
	RV = RVi[:2*QuantityOfRegisters]

	ByteCount = 2 * QuantityOfRegisters
	print "Byte Count: " + str(ByteCount)

	BC = [ByteCount]

	PDU_RESPONSE = FC + BC + RV
	
	print ""
	
	return (PDU_RESPONSE, Registers)



## WRITE MULTIPLE REGISTERS ##

def WriteMultipleRegistersSERVER(PDU, Registers, FirstAddress, NumberOfRegisters):
	# Returns a Tuple with the PDU_response and the Registers Values.
	# If sucessful, writes the values received to the registers requested, and returns the Starting Address
	# and the Quantity of Registers.
	# If not sucessful, returns Function Code 144 (0x90) and the corresponding Exception Code.

	FunctionCode = PDU[0]
	FC = [FunctionCode]

	SA = PDU[1:3]
	StartingAddress = TwoBytesToInt(SA)
	print "Starting Address: " + str(StartingAddress)


	# Tests for illegal values for the Starting Address. Returns Exception Code 2 if founds an error.
	if (StartingAddress < FirstAddress):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 144  #0x90
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be greater or equal to " + str(FirstAddress)
		print ""
		return (PDU_RESPONSE, Registers)

	if (StartingAddress >= (FirstAddress + NumberOfRegisters)):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 144  #0x90
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."
		print "Starting Address must be less or equal to " + str(FirstAddress+NumberOfRegisters-1)
		print ""
		return (PDU_RESPONSE, Registers)

	
	QoR = PDU[3:5]
	QuantityOfRegisters = TwoBytesToInt(QoR)
	print "Quantity Of Registers: " + str(QuantityOfRegisters)

	# Tests for illegal values of Quantity of Registers. If and error is found, generates Exception Code 2.
	if ((QuantityOfRegisters+StartingAddress) > (FirstAddress + NumberOfRegisters)):
		ExceptionCode = 2
		EC = [ExceptionCode]
		FunctionCode = 144  #0x90
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA ADDRESS!"
		print "The data address received in the query is not an allowable address for the server."		
		print "Too much Registers! Must be less or equal to " + str(FirstAddress+NumberOfRegisters-StartingAddress)
		print ""
		return (PDU_RESPONSE, Registers)
	

	ByteCount = PDU[5]
	print "Byte Count: " + str(ByteCount)

	# Tests for Illegal Data Values. Uses the Byte Count information to know how many bytes are expected.
	if (len(PDU) != (ByteCount+6)):
		ExceptionCode = 3
		EC = [ExceptionCode]
		FunctionCode = 144 #0x83
		FC = [FunctionCode]
		PDU_RESPONSE = FC + EC

		print "ERROR!"
		print "Exception Code: " + str(ExceptionCode)
		print "EXCEPTION: ILLEGAL DATA VALUE!"
		print "A value contained in the query data field is not an allowable value for the serve."
		print ""
		return (PDU_RESPONSE, Registers)


	# If no error is found...
	
	RegisterValue = PDU[6:]
	print "Register Value: " + str(RegisterValue)
	
	## Routine to Write to the Registers list ##

	i = (StartingAddress-FirstAddress)*2
	k = 0

	while (k < QuantityOfRegisters*2):
		Registers[i] = RegisterValue[k]
		i = i + 1
		k = k + 1

	## End of Routine ##

	print "Register: " + str(Registers)
	print ""

	PDU_RESPONSE = FC + SA + QoR

	return (PDU_RESPONSE, Registers)

