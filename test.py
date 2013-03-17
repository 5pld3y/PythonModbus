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

########################
## END OF ESC ROUTINE ##
########################

TIME = 100
s = sched.scheduler(time.time, time.sleep)

def modbusSEND(): 
	print "From print_time", time.time()

def loop(FUNCTION, TIME):
	while 1:

		s.enter((TIME/100), 1, FUNCTION, ())
		s.run()

		if kbhit():
			if (ord(getche()) == 27):
				print "q"
				print "ESC Key pressed!"
				break

set_normal_term()
print "XPTO"
abc = raw_input("ABC: ")
print abc

set_curses_term()
loop(modbusSEND, 100)

