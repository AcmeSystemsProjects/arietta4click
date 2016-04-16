import acmepins
import time
import datetime

import sys
import serial
from gps_class import gps

def print_err(*args):
    sys.stderr.write(' '.join(map(str,args)) + '\n')


def reset():
	NanoGPS_RST = acmepins.Pin("J4.33","out")
	NanoGPS_PWR = acmepins.Pin("J4.38","out")
	
	NanoGPS_RST.high()
	time.sleep(0.3)
	NanoGPS_RST.low()
	
	#Accende
	NanoGPS_PWR.low()
	time.sleep(0.1)
	NanoGPS_PWR.high()
	time.sleep(2)
	NanoGPS_PWR.low()
	time.sleep(0.1)
	
	GNSS3_RST = acmepins.Pin("J4.29","out")
	GNSS3_RST.high()

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

#Apre seriale su NanoGPS
NanoGPS_ser = serial.Serial(
    port='/dev/ttyS1', 
    baudrate=4800, 
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)  


#Apre seriale su GSSS3
GNSS3_ser = serial.Serial(
    port='/dev/ttyS2', 
    baudrate=115200, 
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)  


g1=gps('NanoGPS', NanoGPS_ser)
g2=gps('GNSS3', GNSS3_ser)


def print_msg (gx, x):
	# update status
	id=gx.parseLine(x)
	if (id == 'GSA'):
		if (gx.data['AutoSelection'] == 'A'):
			 
			if  (gx.data['3Dfix'] == 2):
				print color['darkyellow'],
				print "%s ***** FIX 2D" % (gx.named),
				print color['off']

			if  (gx.data['3Dfix'] == 3):
				print color['green'],
				print "%s ***** FIX 3D" % (gx.name),
				print color['off']
		
	if (id == 'RMC'):
		if (gx.data['RmcStatus'] == 'A'):
			print color['green'],
			print "%s ***** NAV %.5f %s %.5f %s %s" % (
				gx.name,
				gx.data['Latitude'],
				gx.data['NsIndicator'], 
				gx.data['Longitude'],
				gx.data['EwIndicator'],
				gx.data['Date'],
			)
			print color['off'],
		


				

while True:     
	
	x = g1.ser.readline().rstrip("\r\n")
	
	print_err ("%s %s: %s" % (g1.name, datetime.datetime.now().isoformat(), x))
	sys.stderr.flush()
	
	print_msg(g1, x)
	sys.stdout.flush()
			
			
			
	x = g2.ser.readline().rstrip("\r\n")

	print_err ("%s %s: %s" % (g2.name, datetime.datetime.now().isoformat(), x))
    sys.stderr.flush()
	
	print_msg(g2, x)
	sys.stdout.flush()


