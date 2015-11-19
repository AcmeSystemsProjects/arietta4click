#
# Pushbutton example
# 
# Run with: 
#  python pushbutton.py
#
# Type ctrl-C to exit
#

import acmepins

Button = acmepins.Pin("J4.10","in")

while True:
	if Button.get_value()==0:
		print "Pressed"
	else:
		print "Released"
