# ESP32 BLE RSSI-Based Servo Controller

This project uses an ESP32 to scan for a specific BLE device by MAC address. Based on the Received Signal Strength Indicator (RSSI), the ESP32 controls a servo motor to open or close. The project is designed to open the servo when the target BLE device is within a specific range and close it after the device moves out of range for a set period.

## Project Structure
- **BLE Scanner**: Continuously scans for a target BLE device and measures RSSI to determine proximity.
- **Servo Controller**: Opens the servo if the target device’s RSSI is above a threshold and closes it if the RSSI drops below the threshold and remains there for 10 seconds.
- **ESP8266 Communication**: Sends activation time to an ESP8266 to log or process as needed.

## Features
- Controls a servo motor based on BLE RSSI to simulate proximity-based actions.
- Adjustable RSSI threshold to set proximity sensitivity.
- Activation events are sent to an ESP8266 for further processing or logging.

## Requirements
- **Hardware**:
  - ESP32 (for BLE scanning and servo control)
  - Servo motor
  - ESP8266 (optional, for logging activation events)
- **Libraries**:
  - [ESP32Servo](https://github.com/madhephaestus/ESP32Servo) for servo motor control on the ESP32
  - BLE libraries built into the ESP32 core

## Configuration

### BLE Target MAC Address
Set the target BLE device's MAC address in the code:
```cpp
const String targetAddress = "DC:0D:30:1E:DA:D6";


# ESP8266 Activation Logger with Flask Server

This project uses an ESP8266 to log activation events by sending timestamps to a Flask server. The Flask server records the activation events and logs them in a file on the local desktop. This setup is ideal for monitoring events remotely, such as the activation of a servo or other hardware components.

## Project Structure
- **ESP8266 WiFi Client**: Connects to a WiFi network, listens for activation signals, and sends the activation time to the server.
- **Flask Server**: Receives activation time data from the ESP8266 and logs it to a local `data.txt` file on the desktop.

## Features
- Logs activation times in a readable format.
- Sends HTTP POST requests from ESP8266 to the server.
- Flask server responds to requests and logs the data.

## Requirements
- **Hardware**: ESP8266 microcontroller.
- **Software**: Arduino IDE, Python with Flask installed.
- **Dependencies**:
  - Python 3
  - Flask (`pip install Flask`)

## Setup and Installation

### ESP8266 Code
1. **Configure WiFi Credentials**:
   Edit the ESP8266 code to set your WiFi SSID and password:
   ```cpp
   const char* ssid = "your_ssid";
   const char* password = "your_password";
