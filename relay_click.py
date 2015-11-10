import clickboard
import time
 
print "RELAY click example"
print "Type ctrl-C to exit"

#Use mikroBUS slot #1
mikroBUS = 1 

REL1 = clickboard.RelayClick("REL1",mikroBUS)
REL2 = clickboard.RelayClick("REL2",mikroBUS)
 
while True:
	time.sleep(1)

	REL1.on()
	REL2.off()
	
	time.sleep(1)
	
	REL1.off()
	REL2.on()
