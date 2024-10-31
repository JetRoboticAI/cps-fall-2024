import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class TemperatureListener:
    def __init__(self, broker, port, topic, keepalive=60):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.keepalive = keepalive
        self.client = mqtt.Client()

        # 设置回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.target_temp = 0

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        # 订阅主题
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            # 获取目标温度
            self.target_temp = float(msg.payload.decode())
            print(f"Target temperature received: {self.target_temp}")
            
        except ValueError:
            print("Received an invalid temperature value.")

    def start(self):
        # 连接到 MQTT 代理
        self.client.connect(self.broker, self.port, self.keepalive)
        # 开始循环监听消息
        self.client.loop_start()

    def stop(self):
        # 停止监听并断开连接
        self.client.loop_stop()
        self.client.disconnect()

    def get_target_temperature(self):
        return self.target_temp
    
if __name__ == "__main__":
    broker_address = "broker.hivemq.com"
    port = 1883
    topic = "home/temperature/setpoint"
    
    listener = TemperatureListener(broker_address, 1883, topic)
    listener.start()
    try:
        while True:
            target_temp = listener.get_target_temperature()
            #if target_temp is not None:
                #print(target_temp)
            time.sleep(5)
    except KeyboardInterrupt:
        print("STOP")
        listener.stop()
        
GPIO.cleanup()        