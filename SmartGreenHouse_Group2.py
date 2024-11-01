import dht11
import RPi.GPIO as GPIO
import time
import datetime
import csv
# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the DHT11 data pin
DHT11_PIN = 20
FAN_PIN = 17
LED_PIN = 27
MOTOR_PIN = 21

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Initialize the DHT11 instance
sensor = dht11.DHT11(pin=DHT11_PIN)
# Define thresholds
TEMP_THRESHOLD = 21  # Set desired temperature threshold in Celsius
HUM_THRESHOLD =  55  # Set desired humidity threshold in %

try:
    while True:
        # Read the data from the sensor
        result = sensor.read()
        
        if result.is_valid():
            print(f"Temperature: {result.temperature}°C")
            print(f"Humidity: {result.humidity}%")
            new_data = [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Temperature: ' + str(result.temperature)+ 'C', 'Humidity: ' +str(result.humidity)+'%']]
            with open('data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(new_data)
            # Control fan and LED based on temperature
            if result.temperature > TEMP_THRESHOLD:
                GPIO.output(FAN_PIN, GPIO.HIGH)  # Turn on fan
                GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED alert
                print("Fan ON - Temperature too high!")
            else:
                GPIO.output(FAN_PIN, GPIO.LOW)   # Turn off fan
                GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED alert
                print("Fan OFF - Temperature OK")
           
            # Humidity alert
            if result.humidity < HUM_THRESHOLD:
                GPIO.output(MOTOR_PIN, GPIO.HIGH)
                print("SPRINKLERS ON - Humidity is below the optimal threshold!")
            else:
                GPIO.output(MOTOR_PIN, GPIO.LOW)  
                print("SPRINKLERS OFF - Humidity OK")
           


except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()