##server.py
from socket import *    #import the socket library
from sys import *
server = socket
 
##let's set up some constants
HOST = ""    #we are the host
PORT = 29876    #arbitrary port not currently in use
ADDR = (HOST,PORT)    #we need a tuple for the address
BUFSIZE = 4096    #reasonably sized buffer for data
 
## now we create a new socket object (serv)
## see the python docs for more information on the socket types/flags

# create an AF_INET, STREAM socket (TCP)
server = socket( AF_INET,SOCK_STREAM)
# AF_INET : Adress Family - This is IP version 4 or IPv4.
# SOCK_STREAM : Type - this means connection oriented TCP protocol. 
print "Socket Created!"

try:
	##bind our socket to the address
	server.bind((ADDR))    #the double parens are to create a tuple with one element
except socket.error as msg:
	print "Failed to bind socket."
	print "Error Code: " + str(msg[0])
	print "Error Message: " + str(msg[1])
	sys.exit();
print "Socket Bind complete!"

server.listen(5)    #5 is the maximum number of queued connections we'll allow
print "listening..."
 
conn,addr = server.accept() #accept the connection
print "...connected!"
conn.send("TEST")
 
conn.close()