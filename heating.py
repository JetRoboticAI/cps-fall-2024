
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt


app = Flask(__name__)

# MQTT设置
MQTT_BROKER = "broker.emqx.io"  # 替换为您的MQTT代理地址
MQTT_PORT = 1883
MQTT_TOPIC = "home/temperature/setpoint"  # 替换为您的目标主题

# 创建MQTT客户端
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

# 定义发布消息的函数
def publish_to_mqtt(value):
    message = str(value)
    mqtt_client.publish(MQTT_TOPIC, message)
    print(f"Published '{message}' to topic '{MQTT_TOPIC}'")

# Flask路由，接收HTTP请求并发布消息
@app.route('/publish', methods=['POST'])
def publish_message():
    data = request.get_json()
    value = data.get("value")

    if isinstance(value, int):  # 检查是否为整数
        publish_to_mqtt(value)
        return jsonify({"status": "Message sent to MQTT", "value": value}), 200
    else:
        return jsonify({"error": "Invalid data format. 'value' should be an integer."}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)