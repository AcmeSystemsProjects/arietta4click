import acmepins
import time
import datetime



def reset_nano():
	
	NanoGPS_RST = acmepins.Pin("J4.33","out")
	NanoGPS_PWR = acmepins.Pin("J4.38","out")
	
	NanoGPS_RST.high()
	time.sleep(0.3)
	NanoGPS_RST.low()
	
	print "Resetting NanoGPS......"
	#Accende
	NanoGPS_PWR.low()
	time.sleep(0.1)
	NanoGPS_PWR.high()
	time.sleep(2)
	NanoGPS_PWR.low()
	time.sleep(0.1)

def reset_gnss3():
	print "Resetting GNSS3......"
	GNSS3_RST = acmepins.Pin("J4.29","out")
	GNSS3_RST.high()
	
	time.sleep(0.1)
	
	GNSS3_RST.low()
	
	time.sleep(0.1)
	
	GNSS3_RST.high()

if __name__ == "__main__":

	import sys

	#print 'Number of arguments:', len(sys.argv), 'arguments.'
	#print 'Argument List:', str(sys.argv)
	
	if (len(sys.argv) == 1):
		#
		# reset at least at power on
		#
		reset_nano()
		reset_gnss3()
	else:
		for x in sys.argv:
			print x
			if (x == "nano"): 
				reset_nano()
			if (x == "gnss3"): 
				reset_gnss3()
