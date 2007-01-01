import acmepins
import time
import sys
import serial

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


while True:     
	print "NanoGPS %s" % (NanoGPS_ser.readline())
	print "GNSS3   %s" % (GNSS3_ser.readline())


#while True:     
#    bytesToRead = NanoGPS_ser.inWaiting()
    
#    if bytesToRead>0:
#      value=ser.read(1)
#      sys.stdout.write( '%s' % value )
#      sys.stdout.flush()
 

