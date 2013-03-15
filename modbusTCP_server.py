# modbusTCP_server.py

from binoperations import *

def decodeTCP(TCP):
	TI = TCP[0:2]
	PI = TCP[2:4]
	L = TCP[4:6]
	UI = TCP[6]

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

	TI = intTo2Bytes(TransactionIdentifier)
	PI = intTo2Bytes(0)
	L = intTo2Bytes(Length+1)
	UI = [UnitIdentifier]

	TCP = TI + PI + L + UI
	return TCP

