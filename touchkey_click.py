import clickboard
import time
 
print "Touchkey click example"
print "Type ctrl-C to exit"

#mikroBUS Slot number
mikroBUS = 1 

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

	
	

