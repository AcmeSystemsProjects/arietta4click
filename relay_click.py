#RELAY click example
#Place the RELAY click on mikroBUS 1

import clickboard
import time
 
print "REALY click example"
print "Type ctrl-C to exit"

mikroBUS_id = 1
 
powerline_1 = clickboard.RelayClick("REL1",mikroBUS_id)
powerline_2 = clickboard.RelayClick("REL2",mikroBUS_id)
 
while True:
	time.sleep(1)
	
	powerline_1.on()
	powerline_2.off()
	
	time.sleep(1)
	
	powerline_1.off()
	powerline_2.on()
