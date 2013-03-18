# modbusTCP_server.py

# Imports
from binoperations import *



def decodeTCP(TCP):
	# Fuction used to interpret the TCP of the REQUEST. Returns the Transaction Identifier to be used to construct
	# the TCP of the response.

	TI = TCP[0:2] 				# Transaction Identifier (2 bytes)
	PI = TCP[2:4]				# Protocol Identifier (2 bytes)
	L = TCP[4:6]				# Length (2 bytes)
	UI = TCP[6]					# Unit Identifier (1 byte)

	# The TwoBytesToInt function is called to convert the list of two bytes, represented as int values to a 
	# single int value.
	TransactionIdentifier = TwoBytesToInt(TI)			
	ProtocolIdentifier = TwoBytesToInt(PI)
	Length = TwoBytesToInt(L)
	UnitIdentifier = UI
	
	print "== MBAP Header =="
	print "Transaction Identifier: " + str(TransactionIdentifier)
	print "Protocol Identifier: " + str(ProtocolIdentifier)
	print "Length: " + str(Length)
	print "Unit Identifier: " + str(UnitIdentifier)

	return TransactionIdentifier



def createTCP(TransactionIdentifier = 0, Length = 1, ProtocolIdentifier = 0, UnitIdentifier = 0):
	# Function called to build the TCP layer of the RESPONSE. Returns a list with each byte value represented as an
	# int value.

	# The intTo2Bytes function is called to convert a single int value to a list of two bytes, each represented as 
	# an int value.
	TI = intTo2Bytes(TransactionIdentifier)
	PI = intTo2Bytes(0)
	L = intTo2Bytes(Length+1)
	UI = [UnitIdentifier]

	TCP = TI + PI + L + UI
	return TCP

