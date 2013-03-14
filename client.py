# Client program
import socket
import sys
import modbustcp
import modbusadu
import interface
import select

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


client.setblocking(0)
client.send(modbusadu.modbus(3))

while 1:

    ### Receive Routine ###
    ready = select.select([client], [], [], 0.1)
    
    if ready[0]:
        data = client.recv(4096)
        print data
    ### End of Receive Routine ####

    option = interface.MenuClient()
    print option
    
    if option == "2":
        print "Option 2"
        request = interface.MenuClient_Read()
        client.send(request)
    elif option == "3":
        print "Option 3"
        client.send("XPTO 3")
    elif option == "4":
        print "Option 4"
        client.send(modbusadu.modbus(3))
    else:
        print "abc"
