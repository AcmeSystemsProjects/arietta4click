

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
### time.struct_time(tm_year=2016, tm_mon=6, tm_mday=4, tm_hour=20, tm_min=19, tm_sec=36, tm_wday=5, tm_yday=156, tm_isdst=0)


"""
2.3.22 Packet Type: 335 PMTK_API_SET_RTC_TIME
This command set TC UTC time. To be noted, the command doesn't
update the GPS time which maintained by GPS receiver.
After setting, the RTC UTC time finally may be updated by GPS receiver 
with more accurate time after 60 seconds.

Table 2-33: 335 PMTK_API_SET_RTC_TIME Data Format

DataField: PMTK335,Year,Month,Day,Hour,Min,Sec

Example: $PMTK335,2007,1,1,0,0,0*02<CR><LF>

Name  Unit Default Description
Year  --      --     year
Month --      --     1 ~ 12
Day   --      --     1 ~ 31
Hour  --      --     0 ~ 23
Min   --      --     0 ~ 59
Sec   --      --     0 ~ 59

"""

cmd = "$PMTK335,%d,%d,%d,%d,%d,%d" % (tt.tm_year, tt.tm_mon, tt.tm_mday, tt.tm_hour, tt.tm_min, tt.tm_sec)

#print cmd

chks = calcCheckSum (cmd);

cmd = "%s*%02X" % (cmd , chks)

print cmd

### PMTK001,335,3*35


