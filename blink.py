#
# Blinking led
# 
# Run with: 
#  python blink.py
#
# Type ctrl-C to exit
#

import acmepins
import time

Led = acmepins.Pin("J4.8","low")
 
while (True): 
	Led.on()
	time.sleep(1)
	Led.off()
	time.sleep(1)

