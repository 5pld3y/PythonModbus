# Echo server program
import socket
import sys
import thread

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

def clientthread(conn):
    conn.send("Welcome to the server. Type something and hit enter")

    while 1:
        recieved = conn.recv(1024)
        print recieved
        reply = "OK... " + recieved
        if not recieved:
            break
        conn.sendall(reply)

    conn.close()


while 1:
    conn, addr = server.accept()
    print "Connected with " + addr[0] + ":" + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    thread.start_new_thread(clientthread ,(conn,))

server.close()


    # num = conn.send("Successful connection with server!")
    # #print num # returns the number of bytes sent of method send
    
    # while 1:
    #     data = raw_input ( "SEND( TYPE q or Q to Quit):" )
    #     if (data == 'Q' or data == 'q'):
    #         conn.send (data)
    #         conn.close()
    #         break;
    #     else:
    #         conn.send(data)
 
    #     data = conn.recv(512)
    #     if ( data == 'q' or data == 'Q'):
    #         conn.close()
    #         break;
    #     else:
    #         print "RECIEVED:" , data





    #data = conn.recv(1024)
    #print data

    # reply = "Ok..." + data
    # if not data:
    #     break

    # conn.sendall(reply)
    


conn.close()
server.close()

# conn.send("TEST!")



# while 1:
#     data = conn.recv(1024)
#     if not data: break
#     conn.sendall(data)
# conn.close()