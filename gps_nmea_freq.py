

def calcCheckSum(line):
	"""
	Returns the checksum as a one byte integer value.
	In this case the checksum is the XOR of everything after '$' and before '*'.
	"""
	s = 0
	for c in line[1:]:
		s = s ^ ord(c)
	return s
	
import time
tt = time.gmtime()


"""
MT3333_Platform_NMEA_Message_Specification_for_GPS+GLONASS_V1.00 25 2013-09-26

2.3.19 Packet Type: 314 PMTK_API_SET_NMEA_OUTPUT

Set NMEA sentence output frequencies.
There are totally 19 data fields that present output frequencies for the 19 supported NMEA sentences
individually.

Supported NMEA Sentences:

0  NMEA_SEN_GLL, // GPGLL interval - Geographic Position - Latitude longitude
1  NMEA_SEN_RMC, // GPRMC interval - Recommended Minimum Specific GNSS Sentence
2  NMEA_SEN_VTG, // GPVTG interval - Course Over Ground and Ground Speed
3  NMEA_SEN_GGA, // GPGGA interval - GPS Fix Data
4  NMEA_SEN_GSA, // GPGSA interval - GNSS DOPS and Active Satellites
5  NMEA_SEN_GSV, // GPGSV interval - GNSS Satellites in View



17 NMEA_SEN_ZDA, // GPZDA interval - Time and Date

Supported Frequency Setting
0 - Disabled or not supported sentence
1 - Output once every one position fix
2 - Output once every two position fixes
3 - Output once every three position fixes
4 - Output once every four position fixes
5 - Output once every five position fixes

Example:

$PMTK314,1,1,1,1,1,5,0,0,0,0,0,0,0,0,0,0,0,1,0*2D<CR><LF>

This command set GLL output frequency to be outputting once every 1 
position fix, and RMC to be outputting once every 1 position fix, 
and so on.
You can also restore the system default setting via issue:

$PMTK314,-1*04<CR><LF>

"""

NMEA_SEN_GLL = 0
NMEA_SEN_RMC = 0
NMEA_SEN_VTG = 0
NMEA_SEN_GGA = 5
NMEA_SEN_GSA = 5
NMEA_SEN_GSV = 5
NMEA_SEN_ZDA = 0


cmd = "$PMTK314,%d,%d,%d,%d,%d,%d,0,0,0,0,0,0,0,0,0,0,0,%d,0" % \
(                                                               \
NMEA_SEN_GLL,                                                   \
NMEA_SEN_RMC,                                                   \
NMEA_SEN_VTG,                                                   \
NMEA_SEN_GGA,                                                   \
NMEA_SEN_GSA,                                                   \
NMEA_SEN_GSV,                                                   \
NMEA_SEN_ZDA,                                                   \
)

#print cmd

chks = calcCheckSum (cmd);

cmd = "%s*%02X" % (cmd , chks)

print cmd


# $PMTK001,314,3*36

