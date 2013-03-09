# Echo server program
import socket
import sys

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
ADDR = (HOST,PORT)
BUFSIZE = 4096

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    server = None
    print "Failed to create socket"
    print "Error Code: " + str(msg[0])
    print "Error Message: " + str(msg[1])
    sys.exit();
print "Socket Created!"


try:
    server.bind((ADDR))
except socket.error as msg:
    print "Failed to bind socket."
    print "Error Code: " + str(msg[0])
    print "Error Message: " + str(msg[1])
    sys.exit();
print "Socket Bind complete!"



server.listen(5)
print "listening..."


conn, addr = server.accept()
print 'Connected by', addr
conn.send("TEST!")
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()