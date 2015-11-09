#RELAY click example
#Place the RELAY click on mikroBUS 1

import acmepins
import time
 
print "REALY click example"
print "Type ctrl-C to exit"
 
REL1 = acmepins.Pin('J4.11','out')
REL2 = acmepins.Pin('J4.13','out')
 
while True:
	time.sleep(1)
	REL1.on()
	REL2.off()
	time.sleep(1)
	REL1.off()
	REL2.on()
