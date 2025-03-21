from RPi import GPIO
from threading import Thread
from time import sleep
from display_lcd import lcd, lcd_display_loop
import log_and_send 
import measure_speed 
import sys

try:
	# Initialize the variables
	measure_speed.init()
	log_and_send.init()

	# Getting the consecutive flag from the command line arguments
	consecutive = False
	if len(sys.argv) > 1 and sys.argv[1].lower() == 'true':
		consecutive = True

	# Display the appropriate message based on the mode
	if consecutive:
		lcd.text("Last Speed(o/s):", 1)
	else:
		lcd.text("Last Speed(cm/s):", 1)

	# Separate threads for each function, to run them concurrently
	Thread(target=measure_speed.speed_measure_loop, args=[False, consecutive]).start()
	Thread(target=lcd_display_loop).start()
	Thread(target=log_and_send.log_mqtt_loop).start()

	# Wait for the user to exit
	input("Press Enter to exit...")
except Exception as e:
	print(e)
finally:
	print('Cleaning Up!')
	measure_speed.stop = True

	# Wait for the threads to finish
	sleep(1)

	GPIO.cleanup()
	lcd.clear()
