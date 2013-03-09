# Echo client program
import socket
import sys

HOST = "localhost"    # The remote host
PORT = 50007              # The same port as used by the server
ADDR = (HOST,PORT)
BUFSIZE = 4096

try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
	client = None
	print "Failed to create socket"
	print "Error Code: " + str(msg[0])
	print "Error Message: " + str(msg[1])
	sys.exit();
print "Socket Created!"


try:
	client.connect((HOST, PORT))
except socket.error as msg:
	print "Failed to connect!"
	print "Error code: " + str(msg[0])
	print "Error Message: " + str(msg[1])
	sys.exit();
print "Socket Connected to " + HOST + " on PORT " + str(PORT)

while 1:
    data = client.recv(512)
    if ( data == 'q' or data == 'Q'):
        client.close()
        break;
    else:
        print "RECIEVED:" , data
        data = raw_input ( "SEND( TYPE q or Q to Quit):" )
        if (data != 'Q' and data != 'q'):
            client.send(data)
        else:
            client.send(data)
            client.close()
            break;

# client.send('Hello, world')

# data = client.recv(1024)

# print 'Received', repr(data)