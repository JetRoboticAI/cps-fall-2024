from RPi import GPIO
from time import monotonic, sleep, time

# Set up the GPIO pins
FIRST = 5 
SECOND = 6  
DISTANCE = 0.1  # Distance between the two sensors in meters

GPIO.setmode(GPIO.BCM)  # Set the GPIO mode to BCM
GPIO.setup(FIRST, GPIO.IN)  # Set the first pin as input
GPIO.setup(SECOND, GPIO.IN)  # Set the second pin as input

# Initialize global variables
def init():
	global last_speed, stop
	last_speed = 0  # Variable to store the last measured speed

	# A hacky way to stop the speed measurement loop becuase we are using threads
	# This was needed cause in class we were told to keep execution time in the mind
	stop = False  

# Function to measure speed in a loop
def speed_measure_loop(keep_last=True, consecutive=False):
	global last_speed, stop
	from log_and_send import send_queue  # Import send_queue from log_and_send module

	# Previous state of the sensors
	previous_first = False  
	previous_second = False 

	# Initialize timestamps
	first_s = 0  
	second_s = 0 

	# Variables for execution time measurement
	last_print_time = monotonic()  
	execution_times = []  

	while not stop:
		start_time = monotonic()  # Start time of the loop iteration
		first = not GPIO.input(FIRST)  # Read the state of the first sensor
		second = not GPIO.input(SECOND)  # Read the state of the second sensor

		
		# Sensors constantly give the values, so we have to detect when does the sensor goes from 0 to 1
		if first and not previous_first:
			first_s = monotonic()  # Record the timestamp
			print('First:', first_s)
			if second_s or consecutive:
				if consecutive:
					if first_s - second_s < 0.2:
						continue
					# Calculate speed for consecutive mode
					last_speed = round(1 / (first_s - second_s), 2)
					print(f'Speed: {last_speed} o/s')
					send_queue.append((time(), last_speed, -1))
					second_s = first_s  # As this is consecutive mode, we need to update the second sensor timestamp
				else:
					# Calculate speed based on distance and time difference, s=d/t
					last_speed = round(DISTANCE / (first_s - second_s) * 100, 2)
					print(f'Speed: {last_speed} cm/s')
					send_queue.append((time(), last_speed, 1))
					second_s = 0
				
				if not keep_last and not consecutive:
					first_s = 0  # Reset first sensor timestamp if not keeping last

		# If the second sensor is triggered (non-consecutive mode)
		if not consecutive and second and not previous_second:
			second_s = monotonic()  # Record the timestamp
			print('Second:', second_s)
			if first_s:
				# Calculate speed based on distance and time difference
				last_speed = round(DISTANCE / (second_s - first_s) * 100, 2)
				print(f'Speed: {last_speed} cm/s')
				send_queue.append((time(), last_speed, 0))
				first_s = 0  # Reset first sensor timestamp
				if not keep_last:
					second_s = 0  # Reset second sensor timestamp if not keeping last

		previous_first = first  # Update previous state of the first sensor
		previous_second = second  # Update previous state of the second sensor

		# Measure the execution time of the loop iteration
		end_time = monotonic()
		execution_time = end_time - start_time
		execution_times.append(execution_time)

		# Print the execution time every 60 seconds
		if end_time - last_print_time >= 60:
			min_time = min(execution_times)
			max_time = max(execution_times)
			avg_time = sum(execution_times) / len(execution_times)
			print(f'Execution Time (min,avg,max) us: {round(min_time * 10**6, 2)}, {round(avg_time * 10**6, 2)}, {round(max_time * 10**6, 2)}')
			last_print_time = end_time  # Update last print time
			execution_times = []  # Reset execution times list

		# Sleep to maintain a loop frequency of approximately 1 kHz
		sleep(max(0, 0.001 - (monotonic() - start_time)))
