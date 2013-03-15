# Client Program

import socket
import sys
from modbusADU_client import *
from clientMENU import *
import select

###############
## Constants ##
###############

HOST = "localhost"    # The remote host
PORT = 50007          # The same port as used by the server
ADDR = (HOST,PORT)    # Tuple address with remote host and port
BUFSIZE = 4096        # The Bufsize used in communications

##################
# Creates Socket #
##################

try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
	client = None
	print "Failed to create socket"
	print "Error Code: " + str(msg[0])
	print "Error Message: " + str(msg[1])
	sys.exit();
print "Socket Created!"


###################
# Connects Socket #
###################

try:
	client.connect((HOST, PORT))
except socket.error as msg:
	print "Failed to connect!"
	print "Error code: " + str(msg[0])
	print "Error Message: " + str(msg[1])
	sys.exit();
print "Socket Connected to " + HOST + " on PORT " + str(PORT)


#############
# Main Loop #
#############

client.setblocking(0)

while 1:

    ### Receive Routine ###
    ready = select.select([client], [], [], 0.1)
    
    if ready[0]:
        data = client.recv(4096)
        dataDecoded = decode(data)

        if dataDecoded[0] == 255:
            Connection = SucessfulConnection(dataDecoded)
            FirstAddress = Connection[0]
            NumberOfRegisters = Connection[1]

        else:
            modbus_response_decode(dataDecoded)

    ### End of Receive Routine ####

    request = MenuClient(FirstAddress, NumberOfRegisters)
    
    if ((request != None)  & (request != "close")):
        print "sent"
        client.send(request)

    if request == "close":
        client.close()
        ## FAZER FUNCAO PARA DIZER AO SERVIDOR QUE CLIENTE FECHOU! ##
        break;
    