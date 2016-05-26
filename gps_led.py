import acmepins
import time
import datetime

class Led():
	def __init__(self, pin_r, pin_g, pin_b):
		self.redp   = acmepins.Pin (pin_r,"out")
		self.greenp = acmepins.Pin (pin_g,"out")
		self.bluep  = acmepins.Pin (pin_b,"out")
		self.off()

	def off(self):
		self.redp.on()
		self.greenp.on()
		self.bluep.on()

	def red(self):
		self.redp.off()
		self.greenp.on()
		self.bluep.on()

	def blue(self):
		self.redp.on()
		self.greenp.on()
		self.bluep.off()

	def green(self):
		self.redp.on()
		self.greenp.off()
		self.bluep.on()

	def white(self):
		self.redp.off()
		self.greenp.off()
		self.bluep.off()

		
	def lightgreen (self):
		""" Function doc """
		self.redp.off()
		self.greenp.off()
		self.bluep.on()
		
	def lightblue (self):
		""" Function doc """
		self.redp.on()
		self.greenp.off()
		self.bluep.off()
		
	def light100 (self):
		""" Function doc """
		self.redp.off()
		self.greenp.on()
		self.bluep.on()

if __name__ == "__main__":
	
	led1 = Led ("J4.31","J4.35","J4.33")
	led2 = Led ("J4.21","J4.29","J4.25")
	
	if True:
		led1.red()
		led2.red()
		time.sleep(1)
		
		led1.lightgreen()
		led2.lightgreen()
		time.sleep(1)
		
		led1.light100()
		led2.light100()
		time.sleep(1)
		
		led1.blue()
		led2.blue()
		time.sleep(1)
		
		
		led1.off()
		led2.off()
		time.sleep(1)
		
