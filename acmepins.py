# acmepins.py 
#
# Python functions collection to easily manage the I/O on:
#   ARIETTA G25 SoM (http://www.acmesystems.it/arietta)
#   ARIA G25 SoM (http://www.acmesystems.it/aria) 
#   ACQUA A5 SoM (http://www.acmesystems.it/acqua)
#
# (C) 2015 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__version__ = 'v0.1'

import os.path
import time
import thread
import threading
import select

#Pin to Kernel ID table
pin2kid = {

#Arietta G25
	'J4.7'   :  23, #PA23
	'J4.8'   :  22, #PA22
	'J4.10'  :  21, #PA21
	'J4.11'  :  24, #PA24
	'J4.12'  :  31, #PA31
	'J4.13'  :  25, #PA25
	'J4.14'  :  30, #PA30
	'J4.15'  :  26, #PA26
	'J4.17'  :  27, #PA27
	'J4.19'  :  28, #PA28
	'J4.21'  :  29, #PA29
	'J4.23'  :   0, #PA0
	'J4.24'  :   1, #PA1
	'J4.25'  :   8, #PA8
	'J4.26'  :   7, #PA7
	'J4.27'  :   6, #PA6
	'J4.28'  :   5, #PA5
	'J4.29'  : 	92, #PC28
	'J4.30'  : 	91, #PC27
	'J4.31'  : 	68, #PC4
	'J4.32'  : 	95, #PC31
	'J4.33'  :  67, #PC3
	'J4.34'  :  43, #PB11
	'J4.35'  :  66, #PC2
	'J4.36'  :  44, #PB12
	'J4.37'  :  65, #PC1
	'J4.38'  :  45, #PB13
	'J4.39'  :  64, #PC0
	'J4.40'  :  46, #PB14

#Todo: remove -32 on Aria G25 
#Aria G25
	'N2'  :  96-32,
	'N3'  :  97-32,
	'N4'  :  98-32,
	'N5'  :  99-32,
	'N6'  : 100-32,
	'N7'  : 101-32,
	'N8'  : 102-32,
	'N9'  : 103-32,
	'N10' : 104-32,
	'N11' : 105-32,
	'N12' : 106-32,
	'N13' : 107-32,
	'N14' : 108-32,
	'N15' : 109-32,
	'N16' : 110-32,
	'N17' : 111-32,
	'N18' : 112-32,
	'N19' : 113-32,
	'N20' : 114-32,
	'N21' : 115-32,
	'N22' : 116-32,
	'N23' : 117-32,
	'E2'  : 118-32,
	'E3'  : 119-32,
	'E4'  : 120-32,
	'E5'  : 121-32,
	'E6'  : 122-32,
	'E7'  : 123-32,
	'E8'  : 124-32,
	'E9'  : 125-32,
	'E10' : 126-32,
	'E11' : 127-32,
	'S2'  :  53-32,
	'S3'  :  52-32,
	'S4'  :  51-32,
	'S5'  :  50-32,
	'S6'  :  49-32,
	'S7'  :  48-32,
	'S8'  :  47-32,
	'S9' :   46-32,
	'S10' :  45-32,
	'S11' :  44-32,
	'S12' :  43-32,
	'S13' :  42-32,
	'S14' :  41-32,
	'S15' :  40-32,
	'S16' :  39-32,
	'S17' :  38-32,
	'S18' :  37-32,
	'S19' :  36-32,
	'S20' :  35-32,
	'S21' :  34-32,
	'S22' :  33-32,
	'S23' :  32-32,
	'W9' :   54-32,
	'W10' :  55-32,
	'W11' :  56-32,
	'W12' :  57-32,
	'W13' :  58-32,
	'W14' :  59-32,
	'W15' :  60-32,
	'W16' :  61-32,
	'W17' :  62-32,
	'W18' :  63-32,
	'W20' :  75-32,
	'W21' :  76-32,
	'W22' :  77-32,
	'W23' :  78-32,

#Acqua A5

	'J1.9'	 :	   	1,
	'J1.10'  :   	0,
	'J1.11'  :   	3,
	'J1.12'  :   	2,
	'J1.13'  :   	5,
	'J1.14'  :   	4,
	'J1.15'  :   	7,
	'J1.16'  :   	6,
	'J1.17'  :   	9,
	'J1.18'  :   	8,
	'J1.19'  :  	11,
	'J1.20'  :  	10,
	'J1.21'  :  	13,
	'J1.22'  :  	12,
	'J1.23'  :  	15,
	'J1.24'  :  	14,
	'J1.25'  :  	77,
	'J1.26'  :  	78,
	'J1.27'  :  	75,
	'J1.28'  :  	76,
	'J1.29'  :  	79,
	'J1.30'  :  	74,
	'J1.31'  : 		156,
	'J1.32'  : 		155,
	'J1.33'  :  	25,
	'J1.35'  :  	27,
	'J1.36'  :  	28,
	'J1.37'  :  	29,
	'J1.38'  :  	26,
	'J1.39'  :  	24,
	'J1.40'  : 		116,
	'J1.41'  : 		117,
	'J1.42'  : 		118,
	'J1.43'  : 		119,
	'J1.44'  : 		120,
	'J1.45'  : 		121,
	'J1.46'  : 		122,
	'J1.47'  : 		123,
	'J1.48'  : 		124,
	'J1.49'  : 		125,
	
	 'J2.1'  : 		127,
	 'J2.2'  : 		126,
	 'J2.3'  : 		115,
	 'J2.5'  : 		109,
	 'J2.6'  : 		108,
	 'J2.7'  : 		107,
	 'J2.8'  : 		106,
	 'J2.9'  : 		111,
	'J2.10'  : 		110,
	'J2.11'  : 		113,
	'J2.12'  : 		112,
	'J2.13'  :  	34,
	'J2.14'  : 		114,
	'J2.15'  :  	38,
	'J2.16'  :  	35,
	'J2.17'  :  	39,
	'J2.18'  :  	43,
	'J2.19'  :  	42,
	'J2.23'  :  	36,
	'J2.25'  :  	37,
	'J2.29'  :  	32,
	'J2.31'  :  	33,
	'J2.32'  :  	46,
	'J2.33'  :  	40,
	'J2.34'  :  	47,
	'J2.35'  :  	41,
	'J2.36'  :  	48,
	'J2.37'  :  	44,
	'J2.38'  :  	49,
	'J2.39'  :  	45,
	'J2.40'  :  	50,
	'J2.42'  :  	59,
	'J2.43'  :  	58,
	'J2.44'  :  	57,
	'J2.45'  :  	60,
	'J2.46'  :  	61,

	 'J3.5'  : 		145, #PE17
	 'J3.6'  : 		144, #PE16
	 'J3.7'  : 		147, #PE19
	 'J3.8'  : 		146, #PE18
	 'J3.9'  : 		143, #PE15
	'J3.10'  : 		151, #PE23
	'J3.11'  : 		152, #PE24
	'J3.12'  : 		153, #PE25
	'J3.13'  : 		154, #PE26
	'J3.14'  : 		148, #PE20
	'J3.15'  :  	54,  #PB22
	'J3.16'  :  	55,  #PB23
	'J3.17'  :  	51,  #PB19
	'J3.18'  :  	53,  #PB21
	'J3.19'  :  	56,  #PB24
	'J3.20'  :  	52,  #PB20
	'J3.22'  :  	87,  #PC23
	'J3.23'  :  	89,  #PC25
	'J3.24'  :  	86,  #PC22
	'J3.25'  :  	88,  #PC24
	'J3.26'  :  	90,  #PC26
	'J3.28'  :  	91,  #PC27
	'J3.29'  :  	92,  #PC28
	'J3.30'  :  	94,  #PC30
	'J3.31'  :  	93,  #PC29
	'J3.32'  :  	95,  #PC31
	'J3.33'  :  	17,  #PA17
	'J3.34'  :  	16,  #PA16
	'J3.35'  :  	19,  #PA19
	'J3.36'  :  	18,  #PA18
	'J3.37'  :  	21,  #PA21
	'J3.38'  :  	20,  #PA20
	'J3.39'  :  	23,  #PA23
	'J3.40'  :  	22,  #PA22
	'J3.41'  :  	31,  #PA31
	'J3.42'  :  	30,  #PA30
	'J3.43'  : 		159, #PE31
	'J3.44'  : 		157, #PE29
	'J3.45'  :  	80,  #PC16
	'J3.46'  :  	81,  #PC17
	'J3.47'  :  	82,  #PC18
	'J3.48'  :  	83,  #PC19
	'J3.49'  :  	84,  #PC20
	'J3.50'  :  	85   #PC21
}

pinmode = {
	"out"	: "low",
	"low" 	: "low",
	"high"	: "high",
	"in" 	: "in"
}

def get_version ():
	return __version__

def get_gpio_path(kernel_id):
	kernel_id=kernel_id
	
	iopath="/sys/class/gpio/pio" 
	if kernel_id>=0 and kernel_id<=31:
		iopath="%sA%d" % (iopath,kernel_id-0)
	if kernel_id>=32 and kernel_id<=63:
		iopath="%sB%d" % (iopath,kernel_id-32)
	if kernel_id>=64 and kernel_id<=95:
		iopath="%sC%d" % (iopath,kernel_id-64)
	if kernel_id>=96 and kernel_id<=127:
		iopath="%sD%d" % (iopath,kernel_id-96)
	if kernel_id>=128 and kernel_id<=159:
		iopath="%sE%d" % (iopath,kernel_id-128)
	return iopath		

def get_kernel_id(connector_name,pin_number):
	return pinname2kernelid(connector_name + "." +pin_number)

def export(kernel_id):
	iopath=get_gpio_path(kernel_id)
	if not os.path.exists(iopath): 
		f = open('/sys/class/gpio/export','w')
		f.write(str(kernel_id))
		f.close()

def unexport(kernel_id):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open('/sys/class/gpio/unexport','w')
		f.write(str(kernel_id))
		f.close()

def direction(kernel_id,direct):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/direction','w')
		f.write(direct)
		f.close()

def set_value(kernel_id,value):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/value','w')
		f.write(str(value))
		f.close()

def get_value(kernel_id):
	if kernel_id<>-1:
		iopath=get_gpio_path(kernel_id)
		if os.path.exists(iopath): 
			f = open(iopath + '/value','r')
			a=f.read()
			f.close()
			return int(a)

def set_edge(kernel_id,value):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		if value in ('none', 'rising', 'falling', 'both'):
		    f = open(iopath + '/edge','w')
		    f.write(value)
		    f.close()

def pinname2kernelid(pinname):
	"""
	Return the Kernel ID of any Pin using the MCU name
	or the board name
	"""

	offset=-1
	if pinname[0:2]=="PA":
		offset=32+0
	if pinname[0:2]=="PB":
		offset=32+32
	if pinname[0:2]=="PC":
		offset=32+64
	if pinname[0:2]=="PD":
		offset=32+96
	if pinname[0:2]=="PE":
		offset=32+128

	if offset!=-1:
		return offset+int(pinname[2:4])
	else:	
		return pin2kid[pinname]

def readU8(bus,address,reg):
  result = bus.read_byte_data(address, reg)
  return result

def readS8(bus,address,reg):
	result = bus.read_byte_data(address, reg)
	if result > 127: 
		result -= 256
	return result

def readS16(bus,address,register):
	hi = readS8(bus,address,register)
	lo = readU8(bus,address,register+1)
	return (hi << 8) + lo

def readU16(bus,address,register):
	hi = readU8(bus,address,register)
	lo = readU8(bus,address,register+1)
	return (hi << 8) + lo

def write8(bus,address,reg,value):
	bus.write_byte_data(address,reg,value)

class Pin():
	"""
	Pins related class
	"""
	kernel_id=None
	fd=None

	def __init__(self,pin,mode):
		self.kernel_id=pinname2kernelid(pin)
		export(self.kernel_id)
		direction(self.kernel_id,pinmode[mode])

		iopath=get_gpio_path(self.kernel_id)
		if os.path.exists(iopath): 
			self.fd = open(iopath + '/value','r')

	def high(self):
		set_value(self.kernel_id,1)
		
	def low(self):
		set_value(self.kernel_id,0)

	def on(self):
		set_value(self.kernel_id,1)
		
	def off(self):
		set_value(self.kernel_id,0)

	def set_value(self,value):
		return set_value(self.kernel_id,value)

	def get_value(self):
		return get_value(self.kernel_id)

	def wait_edge(self,fd,callback,debouncingtime):
		# Conver in millisecs
		debouncingtime=debouncingtime/1000.0 
		
		timestampprec=time.time()
		counter=0
		po = select.epoll()
		po.register(fd,select.EPOLLET)
		while True:
			events = po.poll()
			timestamp=time.time()
			if (timestamp-timestampprec>debouncingtime) and counter>0:
				callback()
			counter=counter+1
			timestampprec=timestamp

	def set_edge(self,value,callback,debouncingtime=0):
		if self.fd!=None:
			set_edge(self.kernel_id,value)
			thread.start_new_thread(self.wait_edge,(self.fd,callback,debouncingtime))
			return
		else:		
			thread.exit()

