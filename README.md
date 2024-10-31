# Smart Waste Management System
This project implements a Smart Waste Management System using a Raspberry Pi. It uses an ultrasonic sensor to measure the bin’s fill level, a PIR sensor to detect motion, and a servo motor to open or close the bin automatically when necessary. The system also integrates MQTT for remote monitoring and control, allowing the waste status to be transmitted to a remote MQTT broker securely with SSL/TLS.

## Features
- Automatic Bin Opening: The bin opens when motion is detected, provided the bin is not full.
- Fill Level Detection: An ultrasonic sensor measures the fill level of the bin, which is indicated by LEDs (green, yellow, red).
- MQTT Integration: The bin’s status is published to an MQTT broker for remote monitoring.
- Secure Communication: MQTT communication is secured using SSL/TLS with username and password authentication.

## Hardware Requirements
- Raspberry Pi (any model with GPIO support)
- Ultrasonic Sensor (HC-SR04)
- PIR Sensor
- Servo Motor
- 3 LEDs (Green, Yellow, Red)
- Jumper Wires
- Breadboard

## Pin Configuration
Component | GPIO Pin 
--- | --- 
Ultrasonic TRIG | 	GPIO 23
Ultrasonic ECHO |   GPIO 24
PIR Sensor |  GPIO 18
Servo Motor	| GPIO 25
Green LED	|  GPIO 17
Yellow LED	|  GPIO 27
Red LED	|  GPIO 22

## Software Requirements
- Python 3
- Paho MQTT library
- RPi.GPIO library for GPIO handling on Raspberry Pi

## Install Python Libraries
pip install paho-mqtt RPi.GPIO

## MQTT Configuration
The MQTT configuration connects to the broker.hivemq.com broker with SSL/TLS. Replace the following with your actual MQTT credentials:

- Username: SWMS@mcmaster.ca
- Password: ****

## License
This project is licensed under the MIT License.
