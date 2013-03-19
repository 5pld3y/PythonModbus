# Client Program

# Imports
import socket
import sys
import sched
import time
from modbusADU_client import *
from clientMENU import *


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

# Prints the Initial Menu and returns a Tuple address with remote host and port
ADDR = InitialMENU()


###############
## Constants ##
###############

HOST = ADDR[0]                  # Contains the HOST address
PORT = ADDR[1]                  # Contains the PORT number
BUFSIZE = 4096                  # The Bufsize used in communications

TransactionIdentifier = 0       # Set the initial Transaction Identifier value to 0 (zero)
FirstAddress = 0                # The default First Address (to be actualized if that function is available in the server)
NumberOfRegisters = 65535       # The default Number of Registers (to be actualized if that function is available in the server)

# Initialize a scheduler to be used in the loop commands.
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

# Sets the Client socket to non-blocking mode.
# Results in the Client socket not blocking the code flow.
client.setblocking(0)

# Infinite loop:
while 1:

    ### DATA RECEIVE ROUTINE ###

    # Wait for notification that an input or output channel is ready
    ready = select([client], [], [], 0.1)
    
    if ready[0]:
        try:
            data = client.recv(BUFSIZE)             # Receives the data from the server (in binary).
        except socket.error:
            print ""
            print "CONNECTION ERROR!"
            print ""
            break
        dataDecoded = decode(data)              # Decodes the data received to a list of integers.

        # Test to check if it's the first data packet received (marked with the first value of 255).
        # If it is, calls function SucessfulConnection to deal with the data received.
        # Saves the values of the First Address and the Number of Registers of the server.
        # Some serves might not send this information. If that's the case, see the values defined at Constants
        if dataDecoded[0] == 255:
            Connection = SucessfulConnection(dataDecoded)
            FirstAddress = Connection[0]
            NumberOfRegisters = Connection[1]

        # If it's not the first data packet, deals with it the normal way. As it's a response from the server,
        # calls function modbus_response_decode to deal with the already decoded (into a list) data.
        else:
            modbus_response_decode(dataDecoded)

    ### END OF RECEIVE ROUTINE ####


    ### CLIENT REQUEST ###

    # Calls the MenuClient function, that prints the menu and deals with the user selection, and returns:
    # 1. - The already encoded ADU to be sent to the server as a request;
    # 2. - The string "close", that results in the client socket being terminated;
    # 3. - A list with the following syntax: [ "READLOOP", TIME, StartingAddress, QuantityOfRegisters, EncodedData ],
    #      that results in a Read Loop command.
    # 4. - A list with the following syntax: [ "WRITELOOP", TIME, StartingAddress, QuantityOfRegisters, ByteCount ],
    #      that result in a Write Loop command.

    request = MenuClient(FirstAddress, NumberOfRegisters, TransactionIdentifier)

    # Checks to see if request is a valid value (not None).
    if (request != None):
        # If it is, enter...

        # 1. - request is the already encoded ADU to be sent to the server as a request.
        if ((request != "close") & (request[0] != "READLOOP") & (request[0] != "WRITELOOP")):
            client.send(request[0])
            TransactionIdentifier = TransactionIdentifier + 1

        # 2. - request is == "close", that results in the client socket being terminated.
        if request == "close":
            client.send("close")
            client.close()
            break
        
        # 3. request = [ "READLOOP", TIME, StartingAddress, QuantityOfRegisters, EncodedData ]
        # Read Loop command.
        if request[0] == "READLOOP":                        # if the instruction is for a Read Loop

            TIME = request[1]                               # Get the Time from MenuClient
            StartingAddress = request[2]                    # Get the Starting Address from MenuClient
            QuantityOfRegisters = request[3]                # Get the Quantity of Registers from MenuClient
            EncodedData = request[4]                        # Get the Encoded Data from MenuClient to be used in the first loop iteration.


            while 1:

                set_curses_term()                           # Sets the terminal to "capture a key" mode

                # Sets the client.send action, with argument EncodedData, to be delayed by TIME/100. (TIME is in ms)
                s.enter((TIME/100), 1, client.send, (EncodedData,))         
                
                # Runs the previous setting
                s.run()

                # Prints and increments the Transaction Identifier, to be used in the following Read command.
                print "Transaction Identifier: " + str(TransactionIdentifier)
                TransactionIdentifier = TransactionIdentifier + 1

                # Generates a already encoded ADU, to be used as a request in the following loop iterations.
                MODBUSDirectRequest = modbus(TransactionIdentifier, 3, StartingAddress, QuantityOfRegisters)
                EncodedData = MODBUSDirectRequest[0]


                # Receive Routine #

                # Wait for notification that an input or output channel is ready
                ready = select([client], [], [], 0.1)
        
                if ready[0]:
                    try:
                        data = client.recv(BUFSIZE)             # Receives the data from the server (in binary).
                    except socket.error:
                        print ""
                        print "CONNECTION ERROR!"
                        print ""
                        break
                    dataDecoded = decode(data)              # Decodes the data received to a list of integers.

                # Calls function modbus_response_decode to deal with the already decoded (into a list) data.
                modbus_response_decode(dataDecoded)

                # End of Receive Routine #

                print ""
                print "Press ESC to quit"
                print ""

                # ESC ROUTINE #

                # Checks if ESC is pressed. If it is, terminates the loop.
                if kbhit():
                    if (ord(getche()) == 27):
                        set_normal_term()           # Sets the terminal to normal mode.
                        print "q"
                        print "ESC Key pressed!"
                        break;



                # END of ESC ROUTINE #


        # 4. - request = [ "WRITELOOP", TIME, StartingAddress, QuantityOfRegisters, ByteCount ]
        # Write Loop command
        if request[0] == "WRITELOOP":                       # if the instruction is for a Write Loop

            TIME = request[1]                               # Get the Time from MenuClient
            StartingAddress = request[2]                    # Get the Starting Address from MenuClient
            QuantityOfRegisters = request[3]                # Get the Quantity of Registers from MenuClient
            ByteCount = request[4]                          # Get the Byte Count from MenuClient

            while 1:

                # Prints and increments the Transaction Identifier, to be used in the following Read command.
                print "Transaction Identifier: " + str(TransactionIdentifier)
                TransactionIdentifier = TransactionIdentifier + 1


                set_normal_term()           # Sets the terminal to normal mode

                # Registers Write Routine #

                RegisterValue = []
                i = QuantityOfRegisters
                j = StartingAddress

                while i>0:
                    try:
                        X = intTo2Bytes(int(raw_input("R" + str(j) + ": ")))
                    except ValueError:
                        X = [0, 0]
                    RegisterValue = RegisterValue + X
                    i = i - 1
                    j = j + 1

                # End of Registers Write Routine #

                set_curses_term()           # Sets the terminal to capture a key mode

                # Generates a already encoded ADU, to be used as a request in the following loop iterations.
                MODBUSDirectRequest = modbus(TransactionIdentifier, 16, StartingAddress, QuantityOfRegisters, ByteCount, RegisterValue)
                EncodedData = MODBUSDirectRequest[0]


                # Sets the client.send action, with argument EncodedData, to be delayed by TIME/100. (TIME is in ms)
                s.enter((TIME/100), 1, client.send, (EncodedData,))         

                # Runs the previous setting
                s.run()



                # ESC ROUTINE #
               
                # Checks if ESC is pressed. If it is, terminates the loop.
                if kbhit():
                    if (ord(getche()) == 27):
                        set_normal_term()                   # Sets the terminal to normal mode
                        print "q"
                        print "ESC Key pressed!"
                        break;

                # END of ESC ROUTINE #


    ### END OF CLIENT REQUEST ###
