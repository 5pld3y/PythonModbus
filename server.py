# Server Program
import socket
import sys
import thread
from modbusadu import *


##################
## Initial Menu ##
##################

print ""
print "== Modbus Server =="
PORT = int(raw_input("PORT: "))
FirstAddress = int(raw_input("First Address: "))
NumberOfRegisters = int(raw_input("Number Of Registers: "))
print ""

Registers = [0] * 2 * NumberOfRegisters

#print Registers

print "Do you want to initialize the Registers?"
decision = raw_input("(type Y for Yes) ")

if (decision == 'y' or decision == 'Y'):
    print "Register Initialization"

print ""


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


# Defines Client Threading
def clientthread(conn, Registers):
    conn.send(encode([255, FirstAddress, NumberOfRegisters]))
    
    while 1:
        data = conn.recv(1024)
        dataDecoded = decode(data)
        #reply = "Server Received: " + str(dataDecoded)
        
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


# # Defines Client Send Threading (NOT WORKING)
# def clientthread_send(conn):
#     while 1:
#         data = raw_input ( "SEND( TYPE q or Q to Quit):" )
#         if (data == 'Q' or data == 'q'):
#             conn.send (data)
#             conn.close()
#             break;
#         else:
#             conn.send(data)
#         conn.close()

# # Defines Server Threading (USES TOO MUCH RESOURCES)
# def serverthread():
#     while 1:
#         if (_Getch._Getch() == "s"):
#             print "conn closed"

# # Defines Client Threading
# def clientthread_test(conn):
#     conn.send("Successful connection with server!")

#     while 1:
#         data = conn.recv(1024)
#         reply = "OK... " + data
#         if not data:
#             break
#         print "[" + addr[0] + ":" + str(addr[1]) + "]: " + str(sys.getsizeof(data))

#         conn.sendall(reply)

#     conn.close()



#############
# Main Loop #
#############

while 1:

    conn, addr = server.accept()
    print "Connected with " + addr[0] + ":" + str(addr[1])

    thread.start_new_thread(clientthread ,(conn,Registers))

server.close()
