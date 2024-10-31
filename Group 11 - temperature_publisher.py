import paho.mqtt.client as mqtt
import dht11
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class TemperaturePublisher:
    def __init__(self, broker, port, topic, sensor, pin, keepalive=60):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.sensor = sensor
        self.pin = pin
        self.keepalive = keepalive
        self.client = mqtt.Client()
        self.current_temp = 0

        # 设置连接回调函数
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def start(self):
        # 连接到 MQTT 代理
        self.client.connect(self.broker, self.port, self.keepalive)
        # 启动 MQTT 客户端的循环
        self.client.loop_start()

    def publish_temperature(self):
        
            # 从传感器读取温度数据
        result = self.sensor.read()
        
        if result.temperature is not None and result.temperature >= 10:
            
            self.current_temp = result.temperature
            # 将温度数据转换为字符串并发布
            temperature_str = f"{result.temperature:.2f}"
            self.client.publish(self.topic, temperature_str, retain=True)
            print(f"Published current temperature: {temperature_str}")
            
            return result.temperature
        
            # 每2秒更新一次温度

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        
if __name__ == "__main__":
    broker_address = "broker.hivemq.com"
    port = 1883
    topic = "home/temperature/current"
    
    sensor = dht11.DHT11(4)
    
    publisher = TemperaturePublisher(broker_address, 1883, topic,sensor,4)
    publisher.start()
    try:
        while True:
            #current_temp = publisher.current_temp()
            #print(current_temp)
            publisher.publish_temperature()
            
    except KeyboardInterrupt:
        print("STOP")
        publisher.stop()

