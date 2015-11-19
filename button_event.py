#
# Button event 
#
# Type ctrl-C to exit
#

import acmepins
import time
 
Led = acmepins.Pin("J4.8","low")
Button = acmepins.Pin("J4.10","in")

def timedLed():
	print "Pressed"
	Led.on()
	time.sleep(1)
	Led.off()

Button.set_edge("falling",timedLed,0)

while True:
	time.sleep(1)
