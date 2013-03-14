from binoperations import *

data_list = [255, 255, 2, 3, 4, 5, 6, 3, 0, 4, 0, 5]

TCP = data_list[0:7]
print TCP

PDU = data_list[7:]
print PDU

TransactionIdentifier = TCP[0:2]
ProtocolIdentifier = TCP[2:4]
Length = TCP[4:6]
UnitIdentifier = TCP[6]

FunctionCode = PDU[0]
print FunctionCode

StartingAddress = PDU[1:3]
print StartingAddress
print TwoBytesToInt(StartingAddress)

QuantityOfRegisters = PDU[3:5]
print QuantityOfRegisters
print TwoBytesToInt(QuantityOfRegisters)