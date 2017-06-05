import acmepins
import time
import datetime

def led1_off():
	led_1_red.on()
	led_1_green.on()
	led_1_blue.on()

led_1_red = acmepins.Pin("J4.21","out")
led_1_green = acmepins.Pin("J4.29","out")
led_1_blue = acmepins.Pin("J4.25","out")

led1_off()

while True:
   
	
	led_1_red.off()
	time.sleep(1)
	led_1_red.on()
	time.sleep(1)

	led_1_green.off()
	time.sleep(1)
	led_1_green.on()
	time.sleep(1)
	
	led_1_blue.off()
	time.sleep(1)
	led_1_blue.on()
	time.sleep(1)
	
	
