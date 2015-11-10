#RELAY click example

import clickboard
import time
 
#mikroBUS slot used
mikroBUS_id = 1

print "RELAY click example"
print "mikroBUS slot used: " + str(mikroBUS_id)
print "---------------------------"
print "Type ctrl-C to exit"

powerline_1 = clickboard.RelayClick("REL1",mikroBUS_id)
powerline_2 = clickboard.RelayClick("REL2",mikroBUS_id)
 
while True:
	time.sleep(1)
	
	powerline_1.on()
	powerline_2.off()
	
	time.sleep(1)
	
	powerline_1.off()
	powerline_2.on()
