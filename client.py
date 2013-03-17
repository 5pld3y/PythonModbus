# Client Program

import socket
import sys
from modbusADU_client import *
from clientMENU import *
#from test import *

import sched
import time

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
    atexit.register(set_normal_term)
    set_curses_term()

set_normal_term()

########################
## END OF ESC ROUTINE ##
########################


##################
## Initial Menu ##
##################

ADDR = InitialMENU()   # Tuple address with remote host and port


###############
## Constants ##
###############

HOST = ADDR[0]
PORT = ADDR[1]
BUFSIZE = 4096        # The Bufsize used in communications
TransactionIdentifier = 0
s = sched.scheduler(time.time, time.sleep)

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
	client.connect(ADDR)
except socket.error as msg:
	print "Failed to connect!"
	print "Error code: " + str(msg[0])
	print "Error Message: " + str(msg[1])
	sys.exit();
print "Socket Connected to " + HOST + " on PORT " + str(PORT)


#############
# Main Loop #
#############

client.setblocking(0)

while 1:

    ### Receive Routine ###
    ready = select([client], [], [], 0.1)
    
    if ready[0]:
        data = client.recv(4096)
        dataDecoded = decode(data)

        if dataDecoded[0] == 255:
            Connection = SucessfulConnection(dataDecoded)
            FirstAddress = Connection[0]
            NumberOfRegisters = Connection[1]

        else:
            modbus_response_decode(dataDecoded)

    ### End of Receive Routine ####

    request = MenuClient(FirstAddress, NumberOfRegisters, TransactionIdentifier)

    if ((request != None)  & (request != "close") & (request[0] != "READLOOP")):
        client.send(request[0])
        TransactionIdentifier = TransactionIdentifier + 1

    if request == "close":
        client.close()
        ## FAZER FUNCAO PARA DIZER AO SERVIDOR QUE CLIENTE FECHOU! ##

    if request[0] == "READLOOP":
        TIME = request[1]
        StartingAddress = request[2]
        QuantityOfRegisters = request[3]
        EncodedData = request[4]

        while 1:
            #request == ["READLOOP", Time, StartingAddress, QuantityOfRegisters, request[0]]
            # modbus(TransactionIdentifier, FunctionCode, StartingAddress, QuantityOfRegisters)
            set_curses_term()
            s.enter((TIME/100), 1, client.send, (EncodedData,))         
            s.run()
            print "Transaction Identifier: " + str(TransactionIdentifier)
            TransactionIdentifier = TransactionIdentifier + 1
            MODBUSDirectRequest = modbus(TransactionIdentifier, 3, StartingAddress, QuantityOfRegisters)
            EncodedData = MODBUSDirectRequest[0]


            # Receive Routine #

            ready = select([client], [], [], 0.1)
    
            if ready[0]:
                data = client.recv(4096)
                dataDecoded = decode(data)

            modbus_response_decode(dataDecoded)

            # End of Receive Routine #

            print ""
            print "Press ESC to quit"
            print ""

            # ESC ROUTINE #

            
            if kbhit():
                if (ord(getche()) == 27):
                    set_normal_term()
                    print "q"
                    print "ESC Key pressed!"
                    break;



            # END of ESC ROUTINE #
    
