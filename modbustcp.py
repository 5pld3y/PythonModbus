from binoperations import *

def createTCP(TransactionIdentifier = [0,0], ProtocolIdentifier = [0,0], Length = [0,1], UnitIdentifier = [0]):

	TI = [0,0]
	PI = [0,0]
	L = [0, 1]
	UI = [0]

	TCP = TI + PI + L + UI
	return TCP

def readTCP(TCP):
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


