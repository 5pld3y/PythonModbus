# Server Program

import socket
import sys
import thread
from modbusADU_server import *
from serverMENU import *

#################
## ESC ROUTINE ##
#################

# imports
import sys, termios, atexit
from select import select

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def putch(ch):
    sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

# gets the value of the key pressed
def getche():
    ch = getch()
    putch(ch)
    return ch

# detects a key pressed
def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr <> []

if __name__ == '__main__':
    atexit.register(set_normal_term)
    set_curses_term()

# Set Termninal to Normal
set_normal_term()

########################
## END OF ESC ROUTINE ##
########################

##################
## Initial Menu ##
##################

# Calls the Initial Menu and stores the following variables in a list:
# MENU_LIST = [PORT, FirstAddress, NumberOfRegisters, Registers] 
MENU_LIST = initialMENU() 

# Stores the data passed in the list to single variables
PORT = MENU_LIST[0]
FirstAddress = MENU_LIST[1]
NumberOfRegisters = MENU_LIST[2]
Registers = MENU_LIST[3:]
Registers = Registers[0]


###############
## Constants ##
###############

HOST = ''                 # Symbolic name meaning all available interfaces
ADDR = (HOST,PORT)        # Tuple with the Host Address and the Port
BUFSIZE = 4096            # BUFSIZE used for communications


##################
# Creates Socket #
##################

# Tries to create a socket, if not sucessful, prints the error.
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

# Tries to bind the socket, if no sucessful, prints the error.
try:
    server.bind((ADDR))
except socket.error as msg:
    print "Failed to bind socket!"
    print "Error Code: " + str(msg[0])
    print "Error Message: " + str(msg[1])
    sys.exit();
print "Socket Bind complete!"


############################################################
############################################################


############################
# Defines Client Threading #
############################

def clientthread(conn, Registers, FirstAddress):

    # Sends to the client the FirstAddress and the NumberOfRegisters.
    conn.send(encode([255, FirstAddress, NumberOfRegisters]))
    print ""
    
    while 1:
        data = conn.recv(1024)              # Gets data in bytes
        dataDecoded = decode(data)          # Data is decoded to Python recognized variables

        if not data:
            break
        elif data == "close":
            # Detects if a client disconnected from the server.
            conn.close()
            print "Disconnected from " + addr[0] + ":" + str(addr[1])
            print ""
            break;
        else:
            # Prints the decoded data.
            print "[" + addr[0] + ":" + str(addr[1]) + "]: " + str(dataDecoded)

        # Calls the modbus_decode function to interpret the decoded data received.
        # Function returns a tuple with the ADU to be sent as a response and the actualized Registers list.
        ADU_RESPONSEandRegistersTuple = modbus_decode(dataDecoded, Registers, FirstAddress, NumberOfRegisters)
        
        ADU_response = ADU_RESPONSEandRegistersTuple[0]         # Gets the ADU to be sent as a response.
        Registers = ADU_RESPONSEandRegistersTuple[1]            # Gets the new Registers values.

        # Sends the ADU response to the client
        conn.sendall(ADU_response)

    conn.close()


#############
# Main Loop #
#############

# Calls the serverMENU() function and returns the user input (in a string).
option = serverMENU()

while 1: 

    if option == "2":
        
        print "== [2] Listen =="

        # Server listens for new connections ...
        server.listen(5)
        print "listening on PORT " + str(PORT) + "..."

        while 1:
            # ... if it catches a connection, it connects ...        
            conn, addr = server.accept()
            print "Connected with " + addr[0] + ":" + str(addr[1])
            # ... and starts a new thread to deal with the clients requests.
            thread.start_new_thread(clientthread ,(conn,Registers,FirstAddress))


    elif option == "3":
        # Option to close the Server.
        print "Server Closed!"
        server.close()
        break

    else:
        option = serverMENU()
