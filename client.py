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

    if (request != None):

        if ((request != "close") & (request[0] != "READLOOP") & (request[0] != "WRITELOOP")):
            client.send(request[0])
            TransactionIdentifier = TransactionIdentifier + 1


        if request == "close":
            client.send("close")
            client.close()
            break
        
        if request[0] == "READLOOP":                        # if the instruction is for a Read Loop
            TIME = request[1]                               # Get the Time from MenuClient
            StartingAddress = request[2]                    # Get the Starting Address from MenuClient
            QuantityOfRegisters = request[3]                # Get the Quantity of Registers from MenuClient
            EncodedData = request[4]                        # Get the Encoded Data from MenuClient

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

        if request[0] == "WRITELOOP":
            TIME = request[1]                               # Get the Time from MenuClient
            StartingAddress = request[2]                    # Get the Starting Address from MenuClient
            QuantityOfRegisters = request[3]                # Get the Quantity of Registers from MenuClient                     # Get the Encoded Data from MenuClient
            ByteCount = request[4]

            while 1:

                print "Transaction Identifier: " + str(TransactionIdentifier)
                TransactionIdentifier = TransactionIdentifier + 1


                set_normal_term()
                RegisterValue = []
                i = QuantityOfRegisters
                j = StartingAddress

                while i>0:
                    X = intTo2Bytes(int(raw_input("R" + str(j) + ": ")))
                    RegisterValue = RegisterValue + X
                    i = i - 1
                    j = j + 1
                set_curses_term()


                MODBUSDirectRequest = modbus(TransactionIdentifier, 16, StartingAddress, QuantityOfRegisters, ByteCount, RegisterValue)
                EncodedData = MODBUSDirectRequest[0]

                s.enter((TIME/100), 1, client.send, (EncodedData,))         
                s.run()

                # ESC ROUTINE #

                
                if kbhit():
                    if (ord(getche()) == 27):
                        set_normal_term()
                        print "q"
                        print "ESC Key pressed!"
                        break;



                # END of ESC ROUTINE #


    
