# modbusADU_server.py

# Imports
from modbusTCP_server import *
from modbusPDU_server import *
from binoperations import *



def modbus_decode(dataDecoded, Registers, FirstAddress, NumberOfRegisters):
	# Function called to interpret the already decoded data (into a list) and create the response ADU.

	#############
	## REQUEST ##
	#############

	# copies the passed list.
	ADU = dataDecoded

	# Deals with the TCP (the first 7 bytes)
	TCP = ADU[0:7]

	# decodeTCP returns the Transaction Identifier of the request, and it is used later to create the response ADU.
	TransactionIdentifier = decodeTCP(TCP)

	# Deals with the PDU (the bytes following the TCP)
	PDU = ADU[7:]

	# decodePDU is called to interpret the request PDU, and make changes, if requested, to the Registers. 
	# FirstAddress and NumberOfRegisters are passed as arguments to assist in the procedures.
	# Returns a Tuple with the PDU of the response and the new Registers value (in a list).
	PDU_RESPONSEandRegistersTuple = decodePDU(PDU, Registers, FirstAddress, NumberOfRegisters)

	####################
	## END OF REQUEST ##
	####################

	##############
	## RESPONSE ##
	##############

	# Gets the length of the PDU request, in order to generate the correct TCP Length parameter.
	Length = len(PDU)

	# creates the TCP response with the same Transaction Identifier as the response and a different length, 
	# based on the length of the PDU response.
	TCP = createTCP(TransactionIdentifier, Length)
	
	# Join the TCP response and the PDU response to get the ADU response
	ADU_RESPONSE = TCP + PDU_RESPONSEandRegistersTuple[0]

	# Actualize the Registers values.
	Registers = PDU_RESPONSEandRegistersTuple[1]

	#####################
	## END OF RESPONSE ##
	#####################

	# returns a Tuple with the already encoded ADU response and the actualized Registers values (list).
	return (encode(ADU_RESPONSE), Registers)
