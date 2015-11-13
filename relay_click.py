import clickboard
import time
 
print "RELAY click example"
print "Type ctrl-C to exit"

mikroBUS = 1 

REL1 = clickboard.RelayClick("REL1",mikroBUS)
REL2 = clickboard.RelayClick("REL2",mikroBUS)
 
REL1.on()
REL2.on()

time.sleep(1)

REL1.off()
REL2.off()
