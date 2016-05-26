


class Nmea():
	"""

		
	"""
	
	def __init__(self, name_, ser_):
		return
		
		
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


