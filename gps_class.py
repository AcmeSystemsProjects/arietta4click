import serial
import string
import pprint

class gps():
    """
    --  Source code developed by Dhanish -- Elementz Engineers Guild Pvt Ltd
    --  Released under General Public Licence
    --  Checked using SkyTrack GPS
    """

    # This dict holds the global parsed data
    #data = {}

    def __init__(self, name, ser):
		"""
		:param ser: represents the serial object passed
		:return: None
		"""
		self.name = name
		self.ser = ser
		self.data = {}
		self.sat_vect = [ {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, ]

    def toDecimalDegrees(self, ddmm):
		"""
		Converts a string from ddmm.mmmm or dddmm.mmmm format
		to a float in dd.dddddd format
		"""
		
		#print ddmm # 4150.9850
		splitat = string.find(ddmm, '.') - 2
		#print ddmm[:splitat] # 41
		#print ddmm[splitat:] # 50.9850
		try:
			x=self._float(ddmm[:splitat]) + (self._float(ddmm[splitat:]) / 60.00000)
		except:
			x=0.0
			
		return x

    def _float(self, s):
		"""
		Returns the float value of string s if it exists,
		or None if s is an empty string.
		"""
		try:
			return float(s)
		except:
			return None


    def _int(self, s):
		"""
		Returns the int value of string s if it exists,
		or None if s is an empty string.
		"""
		try:
			return int(s)
		except:
			return None


    def calcCheckSum(self, line):
        """
        Returns the checksum as a one byte integer value.
        In this case the checksum is the XOR of everything after '$' and before '*'.
        """
        s = 0
        for c in line[1:-3]:
            s = s ^ ord(c)
        return s


    def parseRMC(self, fields):
        """
        Parses the Recommended Minimum Specific GNSS Data sentence fields.
        Stores the results in the global data dict.

        """

        # RMC has 12 fields
        assert len(fields) == 13

        # MsgId = fields[0]
        self.data['UtcTime'] = fields[1]
        self.data['RmcStatus'] = fields[2]
        self.data['Latitude'] = self.toDecimalDegrees(fields[3])
        self.data['NsIndicator'] = fields[4]
        self.data['Longitude'] = self.toDecimalDegrees(fields[5])
        self.data['EwIndicator'] = fields[6]
        self.data['SpeedOverGround'] = self._float(fields[7])
        self.data['CourseOverGround'] = self._float(fields[8])
        self.data['Date'] = fields[9]
        self.data['MagneticVariation'] = fields[10]
        self.data['UnknownEmptyField'] = fields[11]
        self.data['RmcMode'] = fields[11]

        # Attend to lat/lon plus/minus signs
        if self.data['NsIndicator'] == 'S':
            self.data['Latitude'] *= -1.0
        if self.data['EwIndicator'] == 'W':
            self.data['Longitude'] *= -1.0

    def parseGSA(self, fields):
        """
        Parses the Recommended Minimum Specific GNSS Data sentence fields.
        Stores the results in the global data dict.

		$GPGSA,A,3,10,16,27,26,08,,,,,,,,3.17,3.03,0.95*04

        """

        # GSA has 18 fields
        #print fields
        if len(fields) != 18: return
       
        # MsgId = fields[0]
        self.data['AutoSelection'] = fields[1]
        self.data['3Dfix'] = self._int(fields[2])
        self.data['sat1'] = fields[3]
        self.data['sat2'] = fields[4]
        self.data['sat3'] = fields[5]
        self.data['sat4'] = fields[6]
        self.data['sat5'] = fields[7]
        self.data['sat6'] = fields[8]
        self.data['sat7'] = fields[9]
        self.data['sat8'] = fields[10]
        self.data['sat9'] = fields[11]
        self.data['sat10'] = fields[12]
        self.data['sat11'] = fields[13]
        self.data['sat12'] = fields[14]
        self.data['PDOP'] = self._float(fields[15])
        self.data['HDOP'] = self._float(fields[16])
        self.data['VDOP'] = self._float(fields[17])

    def parseGSV(self, fields):
		"""
		Parses the Recommended Minimum Specific GNSS Data sentence fields.
		Stores the results in the global data dict.
		
		Field Number:

			1. total number of GSV messages to be transmitted in this group
			2. 1-origin number of this GSV message within current group
			3. total number of satellites in view (leading zeros sent)
				4. satellite PRN number (leading zeros sent)
				5. elevation in degrees (00-90) (leading zeros sent)
				6. azimuth in degrees to true north (000-359) (leading zeros sent)
				7. SNR in dB (00-99) (leading zeros sent) more satellite info quadruples like 4-7 n) checksum

		$GPGSV,3,1,10, 15,65,037,25, 25,24,211,26,29, 53,110,32,32, 39,340,31*7B
		
		$GPGSV,3,3, 
		
		12,11,12,278,, 	4    = SV PRN number
						5    = Elevation in degrees, 90 maximum
						6    = Azimuth, degrees from true north, 000 to 359
						7    = SNR, 00-99 dB (null when not tracking)
		
		32,12,139,,
		14,09,136,,
		15,04,035,
		*73
		
		"""
		
		# GSV has 18 fields
		print fields
		assert len(fields) >= 3
		max_f = len(fields)
		
		# MsgId = fields[0]
		n = self._int(fields[1])
		m = self._int(fields[2])
		
		self.data['nSatInView'] = self._int(fields[3])
		
		sat = { }
		n=n+1
		m=m-1
		print "SAT #%d offset: %d" % ( n, m )
		
		for i in range(0, n):
			if ( (7+(4*i)) <= max_f):
				print i, m
				sat['svprn']   = fields[4+(4*i)]
				sat['elev']    = fields[5+(4*i)]
				sat['azimuth'] = fields[6+(4*i)]
				sat['SNR']     = fields[7+(4*i)]
				self.sat_vect[(m*n)+i] = sat.copy()
			
		print "%s: satellites in view: %d" % (self.name, self.data['nSatInView']) 
		for x in range (0, self.data['nSatInView']):
			print "%d: %s" % (x, self.sat_vect[x])

    def parseLine(self, line):
		"""
		Parses an NMEA sentence, sets fields in the global structure.
		Raises an AssertionError if the checksum does not validate.
		Returns the type of sentence that was parsed.
		"""
		
		# Get rid of the \r\n if it exists
		line = line.rstrip()
		
		try:
			# Validate the sentence using the checksum
			assert self.calcCheckSum(line) == int(line[-2:], 16)
		except:
			return None
			
		# Pick the proper parsing function
		try:
			parseFunc = {
				"$GPRMC": self.parseRMC,
				"$GPGSA": self.parseGSA,
				"$GPGSV": self.parseGSV,
			}[line[:6]]
		except:
			return None
		
		# Call the parser with fields split and the tail chars removed.
		# The characters removed are the asterisk, the checksum (2 bytes) and \n\r.
		parseFunc(string.split(line[:-3], ','))
		
		# Return the type of sentence that was parsed
		return line[3:6]


    def getField(self, fieldname):
        """
        Returns the value of the named field.
        """
        return self.data[fieldname]


    def readGPS(self):
        """
        Returns  GPS lattitude, longitude, date, time
        """
        gps_buf = ''

        while (gps_buf.find('$GPRMC') == -1):
            gps_buf = self.ser.readline()

        print(gps_buf)
        self.parseLine(gps_buf)

        return self.data['Latitude'], self.data['Longitude'], self.data['Date'], self.data['UtcTime']


if __name__ == "__main__":

	"""
		ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=serial.EIGHTBITS,
							parity=serial.PARITY_NONE,
							stopbits=serial.STOPBITS_ONE, timeout=None,
							xonxoff=False, rtscts=False,
							writeTimeout=None, dsrdtr=False,
							interCharTimeout=None)
	"""
	ser = NanoGPS_ser = serial.Serial(	port='/dev/ttyS1', 
										baudrate=4800, 
										timeout=1,
										parity=serial.PARITY_NONE,
										stopbits=serial.STOPBITS_ONE,
										bytesize=serial.EIGHTBITS
										)  
	gps_ser = gps(ser)
	while (True):
		print gps_ser.readGPS()
	
