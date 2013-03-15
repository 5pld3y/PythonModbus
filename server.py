# Server Program

import socket
import sys
import thread
from modbusADU_server import *
from serverMENU import *

##################
## Initial Menu ##
##################

MENU_LIST = initialMENU()

PORT = MENU_LIST[0]
FirstAddress = MENU_LIST[1]
NumberOfRegisters = MENU_LIST[2]
Registers = MENU_LIST[3:]
Registers = Registers[0]


###############
## Constants ##
###############

HOST = ''                 # Symbolic name meaning all available interfaces
ADDR = (HOST,PORT)
BUFSIZE = 4096


##################
# Creates Socket #
##################

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    server = None
    print "Failed to create socket!"
    print "Error Code: " + str(msg[0])
    print "Error Message: " + str(msg[1])
    sys.exit();
print "Socket Created!"

################
# Binds Socket #
################

try:
    server.bind((ADDR))
except socket.error as msg:
    print "Failed to bind socket!"
    print "Error Code: " + str(msg[0])
    print "Error Message: " + str(msg[1])
    sys.exit();
print "Socket Bind complete!"

server.listen(5)
print "listening on PORT " + str(PORT) + "..."


############################################################
############################################################


############################
# Defines Client Threading #
############################

def clientthread(conn, Registers):
    conn.send(encode([255, FirstAddress, NumberOfRegisters]))
    print ""
    
    while 1:
        data = conn.recv(1024)
        dataDecoded = decode(data)
        
        if not data:
            break
        elif ( data == 'q' or data == 'Q'):
            conn.close()
            break;
        else:
            print "[" + addr[0] + ":" + str(addr[1]) + "]: " + str(dataDecoded)

        ADUandRegistersTuple = modbus_decode(dataDecoded, Registers)
        
        ADU_response = ADUandRegistersTuple[0]
        Registers = ADUandRegistersTuple[1]

        conn.sendall(ADU_response)

    conn.close()


#############
# Main Loop #
#############

while 1:

    conn, addr = server.accept()
    print "Connected with " + addr[0] + ":" + str(addr[1])

    thread.start_new_thread(clientthread ,(conn,Registers))

server.close()
