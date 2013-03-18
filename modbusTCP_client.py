# modbusTCP_client.py

# Imports
from binoperations import *

####################
## REQUEST CLIENT ##
####################

def createTCP(TransactionIdentifier = 0, Length = 1, ProtocolIdentifier = 0, UnitIdentifier = 0):
	# This function is used to create the TCP of the request. Returns a list with the TCP Header and
	# the Transaction Identifier.

	# The intTo2Bytes function is called to convert a single int value to a list of two bytes, each represented as 
	# an int value.
	TI = intTo2Bytes(TransactionIdentifier)
	PI = intTo2Bytes(0)
	L = intTo2Bytes(Length+1)
	UI = [UnitIdentifier]

	TCP = TI + PI + L + UI
	return [TCP, TransactionIdentifier]

#####################
## RESPONSE CLIENT ##
#####################

def readTCP(TCP):
	# This function is used to read the TCP of the response.
	TI = TCP[0:2]
	PI = TCP[2:4]
	L = TCP[4:6]
	UI = TCP[6]

	# The TwoBytesToInt function is called to convert the list of two bytes, represented as int values to a 
	# single int value.
	TransactionIdentifier = TwoBytesToInt(TI)
	ProtocolIdentifier = TwoBytesToInt(PI)
	Length = TwoBytesToInt(L)
	UnitIdentifier = UI
