#
# Touchkey Click board example
# 
# Run with: 
#  python touchkey_click.py
#
# Type ctrl-C to exit
#

import clickboard
 
mikroBUS = 1 # Slot number to use (1 or 2) 

KeyA = clickboard.TouchClick("A",mikroBUS)
KeyB = clickboard.TouchClick("B",mikroBUS)
KeyC = clickboard.TouchClick("C",mikroBUS)
KeyD = clickboard.TouchClick("D",mikroBUS)

while True:
	if KeyA.get_value():
		print "Key A"
	if KeyB.get_value():
		print "Key B"
	if KeyC.get_value():
		print "Key C"
	if KeyD.get_value():
		print "Key D"
