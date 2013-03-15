# modbusTCP_client.py

from binoperations import *

####################
## REQUEST CLIENT ##
####################

def createTCP(TransactionIdentifier = 0, Length = 1, ProtocolIdentifier = 0, UnitIdentifier = 0):

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
	TI = TCP[0:2]
	PI = TCP[2:4]
	L = TCP[4:6]
	UI = TCP[6]

	TransactionIdentifier = TwoBytesToInt(TI)
	ProtocolIdentifier = TwoBytesToInt(PI)
	Length = TwoBytesToInt(L)
	UnitIdentifier = UI
