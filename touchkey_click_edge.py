#
# Touchkey Click board example
# using event on state changing
#
# Run with: 
#  python touchkey_click_edge.py
#
# Type ctrl-C to exit
#

import clickboard
 
# Touchkey click on slot 1

KeyA = clickboard.TouchClick("A",1)
KeyB = clickboard.TouchClick("B",1)
KeyC = clickboard.TouchClick("C",1)
KeyD = clickboard.TouchClick("D",1)

# Relay click on slot 2

REL1 = clickboard.RelayClick("REL1",2)
REL2 = clickboard.RelayClick("REL2",2)

def timedREL1(secs=1)
	REL1.on()
	time.sleep(secs)
	REL1.off()
	

KeyA.set_edge("rising",timedREL1())

while True:
	time.sleep(20)
