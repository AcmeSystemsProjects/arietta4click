# clickboard.py 
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

import acmepins

#MikroBUS pins on Arietta4click board

clickname2pin = {
	'arietta4click.1.AN'   : 43, #PB11
	'arietta4click.1.RST'  : 67, #PC3
	'arietta4click.1.CS'   : 31, #PA31
	'arietta4click.1.SCK'  : 23, #PA23
	'arietta4click.1.MISO' : 21, #PA21
	'arietta4click.1.MOSI' : 22, #PA22
	'arietta4click.1.PWM'  : 45, #PB13
	'arietta4click.1.INT'  : 66, #PC2
	'arietta4click.1.RX'   : 1,  #PA1
	'arietta4click.1.TX'   : 0,  #PA0
	'arietta4click.1.SCL'  : 65, #PC1
	'arietta4click.1.SDA'  : 64, #PC0
		
	'arietta4click.2.AN'   : 44, #PB12
	'arietta4click.2.RST'  : 92, #PC28
	'arietta4click.2.CS'   : 30, #PA30
	'arietta4click.2.SCK'  : 23, #PA23
	'arietta4click.2.MISO' : 2,  #PA2
	'arietta4click.2.MOSI' : 22, #PA22
	'arietta4click.2.PWM'  : 46, #PB14
	'arietta4click.2.INT'  : 68, #PC4
	'arietta4click.2.RX'   : 6,  #PA6
	'arietta4click.2.TX'   : 5,  #PA5
	'arietta4click.2.SCL'  : 65, #PC1
	'arietta4click.2.SDA'  : 64, #PC0
}

clickname2pin = {

#MikroBUS pins on Arietta4click board
	"arietta4click.1.RelayClick.REL1" :	"J4.12", #PA31 31
	"arietta4click.1.RelayClick.REL2" :	"J4.38", #PB13 45
	"arietta4click.2.RelayClick.REL1" :	"J4.14", #PA30 30
	"arietta4click.2.RelayClick.REL2" :	"J4.40", #PB14 46 

	"arietta4click.1.TouchkeyClick.A" :	"J4.33", #PC3
	"arietta4click.1.TouchkeyClick.B" :	"J4.34", #PB11
	"arietta4click.1.TouchkeyClick.C" :	"J4.38", #PB13
	"arietta4click.1.TouchkeyClick.D" :	"J4.35", #PC2
	"arietta4click.2.TouchkeyClick.A" :	"J4.29", #PC28
	"arietta4click.2.TouchkeyClick.B" :	"J4.36", #PB12
	"arietta4click.2.TouchkeyClick.C" :	"J4.40", #PB14
	"arietta4click.2.TouchkeyClick.D" :	"J4.31"  #PC4
}

class RelayClick():
	pin=None

	def __init__(self,component_name="REL1",mikroBUS_id=1,acme_board_name="arietta4click",):
		clickname=acme_board_name + "." + str(mikroBUS_id) + ".RelayClick." + component_name
		self.pin = acmepins.Pin(clickname2pin[clickname],"out")

	def on(self):
		self.pin.on()
		
	def off(self):
		self.pin.off()

	def __del__(self):
		self.pin.off()
			
class TouchClick():
	pin=None

	def __init__(self,component_name="A",mikroBUS_id=1,acme_board_name="arietta4click",):
		clickname=acme_board_name + "." + str(mikroBUS_id) + ".TouchkeyClick." + component_name
		self.pin = acmepins.Pin(clickname2pin[clickname],"in")

	def get_value(self):
		return self.pin.get_value()

	def set_edge(self,value="rising",callback,debouncingtime=0):
		self.pin.set_edge(value,callback,debouncingtime)


