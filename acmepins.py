# acmepins.py 
#
# Python functions collection to easily manage the I/O on
# Arietta G25 SoM (http://www.acmesystems.it/arietta)
#
# (C) 2015 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__version__ = 'v0.2'

import os.path
import time
import thread
import threading
import select

#Arietta G25 pin to Kernel ID table

pin2kid = {
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

