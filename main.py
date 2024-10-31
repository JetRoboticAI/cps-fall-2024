import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from gpiozero import Servo

            
TRIG = 23
ECHO = 24

GREEN_LED = 17
YELLOW_LED = 27
RED_LED = 22

SSID = "SEPT SmartLAB 537"
PASSWORD = "****"

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 8883  # Secure port for SSL/TLS
MQTT_TOPIC = "SWMS/CA/ON/L864L8/5b191b82-a6b6-49d3-b382-c38c0798a08c"
MQTT_USERNAME = "SWMS@mcmaster.ca"
MQTT_PASSWORD = "*****"

MQTT_TLS_ENABLED = True


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "RaspberryPiClient")

client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

if MQTT_TLS_ENABLED:
    client.tls_set()

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
PIR_PIN = 5
SERVO_PIN = 18
GPIO.setup(PIR_PIN, GPIO.IN)
servo = Servo(SERVO_PIN)
pir_state = False
angle = 0
bin_status = "Empty" 

last_update_time = 0
alert_interval = 5 * 60 * 60

def move_servo_to_angle(angle):
    servo.value = (angle / 90.0) - 1

def check_motion():
    global pir_state, bin_status
    pir_val = GPIO.input(PIR_PIN)
    if pir_val == 1:
        print(pir_state)
        if not pir_state and (bin_status == "Empty" or bin_status == "Partially Full"):
            
            print("Motion detected and bin not full. Opening bin.")
            for angle in range(0, 91, 10): 
                move_servo_to_angle(angle)
                time.sleep(0.05)  
            pir_state = True
        elif bin_status == "Full":
            print("Motion detected but bin is full. Not opening bin.")
    
    else: 
        if pir_state:
            print("Motion ended. Closing bin.")
            for angle in range(90, -1, -10): 
                move_servo_to_angle(angle)
                time.sleep(0.05)
            pir_state = False
            
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

def connect_to_mqtt():
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True) 
    time.sleep(0.00001)  
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    return round(distance, 2)


def update_leds(distance):
    if distance > 50 and distance < 1200:
        GPIO.output(GREEN_LED, GPIO.HIGH)
        GPIO.output(YELLOW_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.LOW)
        return "Empty"
    elif 20 < distance <= 50:
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(YELLOW_LED, GPIO.HIGH)
        GPIO.output(RED_LED, GPIO.LOW)
        return "Partially Full"
    elif 0 < distance <= 20 or distance  > 1200 :
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(YELLOW_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.HIGH)
        return "Full"

def send_mqtt_message(message):
    if client.is_connected():
        client.publish(MQTT_TOPIC, message)
        print(f"Sent alert: {message}")

def main():
    connect_to_mqtt()

    global last_update_time

    try:
        while True:
            distance = measure_distance()
            print(f"Distance: {distance} cm")

            bin_status = update_leds(distance)
            pir_state = False
            
            check_motion()

            if bin_status == "Full":
                send_mqtt_message("Alert: The bin is FULL. Immediate attention needed!")

            if time.time() - last_update_time > alert_interval:
                send_mqtt_message(f"Bin Status: {bin_status}")
                last_update_time = time.time()

            time.sleep(2)

    except KeyboardInterrupt:
        print("Cleaning up...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
