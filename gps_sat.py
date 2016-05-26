import string
import pprint
from nmea import Nmea

n = Nmea(0, 0)

class SatView():
	"""

		name : is the receiver name/identifier
		id   : is the GNSS system (GP: GPS, GN: GLONASS, GL: Galileo

	"""
	def __init__(self, name_, id_):
		self.name = name_
		self.id = id_
		self.init()
		
	def init(self):
		self.sat       = {}
		self.tmp 	   = {}
		self.n_sat_inv = 0
		self.n_sent    = 0
		self.n_seq     = 0
		
	def add(self, svprn, snr, azimuth, elev):
		self.tmp [svprn] = { 'snr': snr, 'azimuth': azimuth, 'elev': elev }
		
	def process (self, s):
		"""
$GPGSV,3,1,12,02,35,287,29,06,40,224,28,07,70,167,20,30,42,197,20*7C
$GPGSV,3,2,12,12,67,210,,09,61,047,,57,55,217,,23,32,068,*7F
$GPGSV,3,3,12,04,21,237,,16,14,048,,05,14,308,,03,08,127,*71
		
		
			$GPGSV,1,1,04,30,,,28,05,,,13,02,,,23,06,,,23*77
			GNSS3: satellites in view: 4
			{   '02': {   'SNR': '23', 'azimuth': '', 'elev': '', 'svprn': '02'},
				'05': {   'SNR': '13', 'azimuth': '', 'elev': '', 'svprn': '05'},
				'06': {   'SNR': '23', 'azimuth': '', 'elev': '', 'svprn': '06'},
				'30': {   'SNR': '28', 'azimuth': '', 'elev': '', 'svprn': '30'}}
		
		"""
		
		#print ">>>> [%s]" % s[:-3]
		
		if s[3:6] != 'GSV': return None
		
		f = string.split(s[:-3], ',')
		max_f = len(f)
		#print f
		
		if max_f < 4: return None

		nsent = int(f[1]) # number of sentences, e.g. : 3
		nmsg  = int(f[2]) # current message, e.g. 2 (1..3)
		
		#print nsent, nmsg
		
		if nmsg == 1:   # this is the first message
			self.tmp = {}
		
		
		#print nsent, nmsg, max_f
		
		#
		# scan message inside current line
		#
		
		for i in range(0, 4):   # [0, 1, 2, 3] as the max number of sat in a msg is 4

			if ( (7+(4*i)) <= max_f):
				print i
				print f[4+(4*i)]
				print f[7+(4*i)]
				print f[6+(4*i)]
				print f[5+(4*i)]
				
				self.add ( 	f[4+(4*i)], # svprn
							f[7+(4*i)], # snr
							f[6+(4*i)], # azimuth
							f[5+(4*i)], # elevation
				)

		if (nmsg == nsent):   # this is the last message 
			self.sat = self.tmp
			self.n_sat_inv = int(f[3])
			
		
		
	def get_tbl (self):
		if len(self.sat):
			return self.sat
		else:
			return None



sv = {
	'NanoG':	{
					'GP': SatView ('NanoG', 'GP'),
					'GN': SatView ('NanoG', 'GN'),
					'GL': SatView ('NanoG', 'GL'),
				},
	'GNSS3':	{
					'GP': SatView ('GNSS3', 'GP'),
					'GN': SatView ('GNSS3', 'GN'),
					'GL': SatView ('GNSS3', 'GL'),
				}
}

if __name__ == "__main__":
	import sys
	import os
	
	newin = os.fdopen(sys.stdin.fileno(), 'r', 80)

	screen = { 'GP': {} , 'GN': {} , 'GL': {} , }

	i = 0

	for line in newin:
		
		line = line.rstrip()
		line = filter(lambda x: x in string.printable, line)
		
		f = string.split(line, ' ')

		#print f
		sys.stdout.flush()
		
		if len(f) == 1:
			rx = sys.argv[1]
			m = line
		else:	
			if len(f) == 3:
				rx = f[0]
				m = f[2]
			else:
				continue

			
		# get the system id (GPS, GLONASS, Galileo...)
		sid = m[1:3]
			
		#print sid, m
		
		# checksum
		try:
			if n.calcCheckSum(m) != int(m[-2:], 16) :
				print ">>>>>>> Wrong checksum: [%d] [%s]" % (int(m[-2:], 16), m[-2:])
				continue
		except:
			continue
		
		if rx in sv:
			
			if sid in sv[rx]:
				x = sv[rx][sid]
				
				x.process(m)
			
				t = x.get_tbl ()
				if t: 
					screen[sid]['data'] = t
					screen[sid]['name'] = x.name
					screen[sid]['nsat'] = x.n_sat_inv
				
		#print screen

		if i % 20 == 0:
			print(chr(27)+"[2J"+chr(27)+"[H"),
					
			for k in screen:
				if screen[k] == {}: continue 
				
				#print "%s: constellation %s: satellites in view: %d" % (screen[k]['name'], sid, screen[k]['n_sat_inv'] ) 
				pp=pprint.PrettyPrinter(indent=4)
				pp.pprint (screen[k]['data'])
				sys.stdout.flush()
		
		i = i + 1
