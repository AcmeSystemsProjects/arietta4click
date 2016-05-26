import acmepins
import time
import datetime

import sys
import serial
#from gps_class import gps
#from gps_led   import Led

#led1 = Led ("J4.31","J4.35","J4.33")
#led2 = Led ("J4.21","J4.29","J4.25")

def print_err(*args):
	sys.stderr.write(' '.join(map(str,args)) + "\n")
	sys.stderr.flush()


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



# Apre seriale su NanoGPS
NanoGPS_ser = serial.Serial(
    port='/dev/ttyS1', 
    baudrate=4800, 
    timeout=.1,
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


#g1=gps('NanoG', NanoGPS_ser)
#g2=gps('GNSS3', GNSS3_ser)


while True:     

	if NanoGPS_ser.inWaiting():
		x = NanoGPS_ser.readline().rstrip("\r\n")
		if len(x): print_err ("%s %s %s" % ('NanoG', datetime.datetime.now().isoformat(), x))

	x = GNSS3_ser.readline().rstrip("\r\n")
	if len(x): print_err ("%s %s %s" % ('GNSS3', datetime.datetime.now().isoformat(), x))
