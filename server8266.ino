#include <ESP8266WiFi.h>
#include <WiFiClient.h>

// WiFi credentials
const char* ssid = "TP-Link_9BA0_5G";
const char* password = "367214C72DF9";

// Server configuration
const char* server = "192.168.0.112";
const int port = 5000;

void setup() {
    Serial.begin(9600);       // Communication with ESP32
    Serial1.begin(115200);    // Communication with Serial Monitor

    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial1.println("Connecting to WiFi...");
    }
    Serial1.println("Connected to WiFi");
}

void loop() {
    // Check if there's data from ESP32
    if (Serial.available()) {
        String data = Serial.readStringUntil('\n');

        // Check if data contains activation time
        if (data.startsWith("ACTIVATION_TIME:")) {
            String activationTime = data.substring(16);
            sendActivationTime(activationTime);
        }
    }
}

void sendActivationTime(String activationTime) {
    WiFiClient client;
    if (client.connect(server, port)) {
        Serial1.println("Connected to server");

        // Construct JSON payload
        String jsonPayload = "{\"activation_time\":\"" + activationTime + "\"}";

        // Send HTTP POST request with JSON payload
        client.println("POST / HTTP/1.1");
        client.println("Host: 192.168.0.112");
        client.println("Content-Type: application/json");
        client.print("Content-Length: ");
        client.println(jsonPayload.length());
        client.println();  // End of headers
        client.print(jsonPayload);
        client.println();

        // Check server response
        while (client.connected() || client.available()) {
            if (client.available()) {
                String response = client.readString();
                Serial1.println("Server response:");
                Serial1.println(response);
                break;
            }
        }

        client.stop();
    } else {
        Serial1.println("Connection to server failed");
    }
}
