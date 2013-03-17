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
def getche():
    ch = getch()
    putch(ch)
    return ch
def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr <> []

if __name__ == '__main__':
    #atexit.register(set_normal_term)
    set_curses_term()

set_normal_term()

########################
## END OF ESC ROUTINE ##
########################

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


############################################################
############################################################


############################
# Defines Client Threading #
############################

def clientthread(conn, Registers, FirstAddress):
    conn.send(encode([255, FirstAddress, NumberOfRegisters]))
    print ""
    
    while 1:
        data = conn.recv(1024)
        dataDecoded = decode(data)

        if not data:
            break
        elif data == "close":
            conn.close()
            print "Disconnected from " + addr[0] + ":" + str(addr[1])
            print ""
            break;
        else:
            print "[" + addr[0] + ":" + str(addr[1]) + "]: " + str(dataDecoded)

        ADUandRegistersTuple = modbus_decode(dataDecoded, Registers, FirstAddress, NumberOfRegisters)
        
        ADU_response = ADUandRegistersTuple[0]
        Registers = ADUandRegistersTuple[1]

        conn.sendall(ADU_response)

    conn.close()


#############
# Main Loop #
#############

option = serverMENU()

while 1: 

    if option == "2":
        
        print "== [2] Listen =="

        server.listen(5)
        print "listening on PORT " + str(PORT) + "..."

        while 1:        
            conn, addr = server.accept()
            print "Connected with " + addr[0] + ":" + str(addr[1])
            thread.start_new_thread(clientthread ,(conn,Registers,FirstAddress))


    elif option == "3":
        print "Server Closed!"
        server.close()
        break

    else:
        option = serverMENU()
