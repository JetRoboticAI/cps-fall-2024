#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <ESP32Servo.h>

// Target device MAC address
const String targetAddress = "DC:0D:30:1E:DA:D6";

int scanTime = 5;  // Scan duration in seconds
BLEScan *pBLEScan;

// Servo configuration
Servo myServo;
const int servoPin = 15;
const int openAngle = 180;
const int closeAngle = 0;
const int rssiThreshold = -60;

bool isServoOpen = false;
unsigned long openTime = 0;

// Servo control functions
void openServo() {
    Serial.println("Opening Servo to 180 degrees");
    myServo.write(openAngle);
    openTime = millis();

    // Send activation time to ESP8266
    Serial2.print("ACTIVATION_TIME:");
    Serial2.println(openTime);
}

void closeServo() {
    Serial.println("Closing Servo to 0 degrees");
    myServo.write(closeAngle);
}

// BLE Callback class
class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
        String deviceAddress = String(advertisedDevice.getAddress().toString().c_str());

        if (deviceAddress.equalsIgnoreCase(targetAddress)) {
            int rssi = advertisedDevice.getRSSI();
            Serial.print("Found target device. RSSI: ");
            Serial.println(rssi);

            if (rssi > rssiThreshold && !isServoOpen) {
                Serial.println("RSSI above threshold - Opening Servo");
                openServo();
                isServoOpen = true;
            } else if (rssi <= rssiThreshold && isServoOpen && millis() - openTime >= 10000) {
                Serial.println("RSSI below threshold and 10 seconds passed - Closing Servo");
                closeServo();
                isServoOpen = false;
            }
        }
    }
};

void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, 16, 17);  // Define custom RX/TX pins for Serial2

    BLEDevice::init("");
    pBLEScan = BLEDevice::getScan();
    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
    pBLEScan->setActiveScan(true);
    Serial.println("Scanning for target device by address...");

    myServo.attach(servoPin);
    closeServo();
}

void loop() {
    pBLEScan->start(scanTime, false);
    delay(2000);
}
