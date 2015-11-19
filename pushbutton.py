#
# Pushbutton example
# 
# Run with: 
#  python pushbutton.py
#
# Type ctrl-C to exit
#

import acmepins
 
button = acmepins.Pin("J4.10","in")

while True:
	if button.get_value():
		print "Pressed"
	else:
		print "Released"
