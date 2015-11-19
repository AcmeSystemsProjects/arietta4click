#
# Pushbutton example
# 
# Run with: 
#  python pushbutton.py
#
# Type ctrl-C to exit
#

import acmepins
 
button = clickboard.TouchClick("A",mikroBUS)

while True:
	if button.get_value():
		print "Pressed"
	else
		print "Released"
