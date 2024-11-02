const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const mqtt = require('mqtt');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const port = 3000;
const mqttClient = mqtt.connect('mqtt://broker.hivemq.com');

mqttClient.on('connect', function () {
    console.log('Connected to MQTT Broker');
    mqttClient.subscribe('TunerSynth769/Readings', function (err) {
        if (!err) {
            console.log('Subscribed to Readings topic');
        }
    });
});

mqttClient.on('message', function (topic, message) {
    console.log(`Received message: ${message.toString()}`);
    wss.clients.forEach(function each(client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(message.toString());
        }
    });
});

//let recordingToggle = true;

app.get('/publish', (req, res) => {
    const message = 'record';
//    recordingToggle = !recordingToggle;

    mqttClient.publish('TunerSynth769/Record', message, (err) => {
        if (!err) {
            res.send('Message sent: ' + message);
        } else {
            res.status(500).send('Failed to send message');
        }
    });
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});