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
    print "Failed to create socket!"
    print "Error Code: " + str(msg[0])
    print "Error Message: " + str(msg[1])
    sys.exit();
print "Socket Created!"


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


while 1:
    conn, addr = server.accept()
    print "Connected with " + addr[0] + ":" + str(addr[1])

    num = conn.send("Successful connection with server!")
    print num # returns the number of bytes sent of method send
    data = conn.recv(1024)
    # reply = "Ok..." + data
    # if not data:
    #     break

    # conn.sendall(reply)
    print data

conn.close()
server.close()

# conn.send("TEST!")



# while 1:
#     data = conn.recv(1024)
#     if not data: break
#     conn.sendall(data)
# conn.close()