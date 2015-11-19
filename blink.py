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

GREEN = acmepins.Pin("J4.8","out")
 
while (True): 
	GREEN.on()
	time.sleep(1)
	GREEN.off()
	time.sleep(1)

