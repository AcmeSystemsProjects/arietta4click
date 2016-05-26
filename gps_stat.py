import acmepins
import time
import datetime

import sys
import serial
from gps_class import gps
#from gps_led   import Led

#led1 = Led ("J4.31","J4.35","J4.33")
#led2 = Led ("J4.21","J4.29","J4.25")

def print_err(*args):
	sys.stderr.write(' '.join(map(str,args)) + "\n")
	sys.stderr.flush()


#
# DO NOT reset (done in/etc/rc.local  at power on)
#
######### reset()


color = {
    'white':    "\033[1;37m",
    'yellow':   "\033[1;33m",
    'green':    "\033[1;32m",
    'blue':     "\033[1;34m",
    'cyan':     "\033[1;36m",
    'red':      "\033[1;31m",
    'magenta':  "\033[1;35m",
    'black':      "\033[1;30m",
    'darkwhite':  "\033[0;37m",
    'darkyellow': "\033[0;33m",
    'darkgreen':  "\033[0;32m",
    'darkblue':   "\033[0;34m",
    'darkcyan':   "\033[0;36m",
    'darkred':    "\033[0;31m",
    'darkmagenta':"\033[0;35m",
    'darkblack':  "\033[0;30m",
    'off':        "\033[0;0m"
}

# Apre seriale su NanoGPS
NanoGPS_ser = serial.Serial(
    port='/dev/ttyS1', 
    baudrate=4800, 
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)  


# Apre seriale su GSSS3
GNSS3_ser = serial.Serial(
    port='/dev/ttyS2', 
    baudrate=115200, 
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)  


g1=gps('NanoG', NanoGPS_ser)
g2=gps('GNSS3', GNSS3_ser)


def print_msg (gx, x):
	# update status
	id=gx.parseLine(x)

	if (id == 'GSA'):
		if (gx.data['AutoSelection'] == 'A'):
			 
			if  (gx.data['3Dfix'] == 2):
				print "%s[%s] ***** FIX 2D%s" % (color['darkyellow'],gx.name,color['off'])
			if  (gx.data['3Dfix'] == 3):
				print "%s[%s] ***** FIX 3D%s" % (color['green'],gx.name,color['off'])
				
				
	if (id == 'RMC'):
		if (gx.data['RmcStatus'] == 'A'):
			print "%s%s ***** NAV %.5f %s %.5f %s %s%s" % (
				color['green'],
				gx.name,
				gx.data['Latitude'],
				gx.data['NsIndicator'], 
				gx.data['Longitude'],
				gx.data['EwIndicator'],
				gx.data['Date'],
				color['off']
			)
			
	if (id == 'GGA'):
		if ((gx.data['PosFixIndicator'] == 1) or (gx.data['PosFixIndicator'] == 1)):
			print "%s%s ***** NAV %.5f %s %.5f %s Time: %s Sat: %d%s" % (
				color['green'],
				gx.name,
				gx.data['Latitude'],
				gx.data['NsIndicator'], 
				gx.data['Longitude'],
				gx.data['EwIndicator'],
				gx.data['UtcTime'],
				gx.data['SatellitesUsed'],
				color['off']
			)

	sys.stdout.flush()
		


				

while True:     
	
	x = g1.ser.readline().rstrip("\r\n")
	
	print_err ("%s %s: %s" % (g1.name, datetime.datetime.now().isoformat(), x))
	
	print_msg(g1, x)
			
#	if ('3Dfix' in g1.data and g1.data['3Dfix'] == 3): 
#		led1.green()
#	else:
#		led1.off()	

			
	x = g2.ser.readline().rstrip("\r\n")

	print_err ("%s %s: %s" % (g2.name, datetime.datetime.now().isoformat(), x))
	
	print_msg(g2, x)

#	if ('3Dfix' in g1.data and g1.data['3Dfix'] == 3): 
#		led1.green()
#	else:
#		led1.off()	

