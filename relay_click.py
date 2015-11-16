#
# Relay Click board example
# 
# Run with: 
#  python relay_click.py
#
# Type ctrl-C to exit
#

import clickboard
import time

mikroBUS = 1 # Slot number to use (1 or 2) 

REL1 = clickboard.RelayClick("REL1",mikroBUS)
REL2 = clickboard.RelayClick("REL2",mikroBUS)
 
REL1.on()
REL2.on()

time.sleep(1)

REL1.off()
REL2.off()

