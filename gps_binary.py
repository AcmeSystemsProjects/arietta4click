import acmepins
import time
import datetime

def calcCheckSum(line):
	"""
	Returns the checksum as a one byte integer value.
	In this case the checksum is the XOR of everything after '$' and before '*'.
	"""
	s = 0
	for c in line[1:]:
		s = s ^ ord(c)
	return s

cmd = "$PMTK253,1,115200"

#print cmd

chks = calcCheckSum (cmd);

cmd = "%s*%02X" % (cmd , chks)

print cmd

### PMTK001,335,3*35
