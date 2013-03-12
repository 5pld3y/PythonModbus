# Client program
import socket
import sys
import modbustcp
import modbusadu
import interface

HOST = "localhost"    # The remote host
PORT = 50007              # The same port as used by the server
ADDR = (HOST,PORT)
BUFSIZE = 4096


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

# while 1:
#     data = client.recv(1024)
#     if ( data == 'q' or data == 'Q'):
#         client.close()
#         break;
#     else:
#         print "RECIEVED:" , data
#         data = raw_input ( "SEND( TYPE q or Q to Quit):" )
#         if (data != 'Q' and data != 'q'):
#             #client.send(data)
#             send(client, "ABC")
#         else:
#             client.send(data)
#             client.close()
#             break;


client.send(modbusadu.modbus(3))

while 1:
    data = client.recv(1024)
    print data

    option = interface.MenuClient()
    print option

    # if (option == 2):
    # 	print "pasdas"
    # else:
    # 	print "asdadsads"
    
    #if request != None:
    #	client.send(request)
