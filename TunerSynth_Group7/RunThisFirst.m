%Run this file before starting the other program
mqClient=mqttclient("mqtt://broker.hivemq.com")
 mySub=subscribe(mqClient,"TunerSynth769/Record")