from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback, PNStatusCategory
import RPi.GPIO as GPIO
import time
from cryptography.fernet import Fernet
import json
import csv

GPIO.setmode(GPIO.BCM)
led_pins = [17, 27, 22, 23]
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-f564a900-4f5e-48df-8e24-5580aa48cf59"
pnconfig.subscribe_key = "sub-c-76a8dc4d-28dc-4468-ba6b-9f4ab714a7a3"
pnconfig.user_id = "minhao"

pubnub = PubNub(pnconfig)

channel_name = "Channel-Barcelona"

def publish_callback(result, status):
    if status.is_error():
        print(status.status_code, status.error_data.__dict__)
    else:
        print(result.timetoken)

my_listener = SubscribeListener()
pubnub.add_listener(my_listener)
pubnub.subscribe().channels(channel_name).execute()
my_listener.wait_for_connect()
GPIO.output(led_pins[3], GPIO.HIGH)
print("connect successfully")

hard_coded_key = b'gkmrxaiQZVDTGKl1Cqv_3to8ZqhJ6wQFzGt6uoeRfRk='
def decrypt(encrypted_data):
    global hard_coded_key
    cipher = Fernet(hard_coded_key)
    decrypted_data = cipher.decrypt(encrypted_data)
    data = json.loads(decrypted_data.decode('utf-8'))
    return data

def light_control(message, speaker):
    words = message.split()
    if 'turn' in words and 'on' in words:
        if speaker == 'eric':
            GPIO.output(led_pins[0], GPIO.HIGH)
            print(f"{speaker}: {message}")
        elif speaker == 'azadi':
            GPIO.output(led_pins[0], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_pins[1], GPIO.HIGH)
            print(f"{speaker}: {message}")
        elif speaker == 'minhao':
            GPIO.output(led_pins[0], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_pins[1], GPIO.HIGH)
            time.sleep(1)
            GPIO.output(led_pins[2], GPIO.HIGH)
            print(f"{speaker}: {message}")
        else:
            print("Unknown speaker, try again")
    
    if 'turn' in words and 'off' in words:
        for pin in led_pins[0:3]:
            GPIO.output(pin, GPIO.LOW)
        
        print(f"{speaker}: {message}")

while True:
    received_messsage = my_listener.wait_for_message_on(channel_name)
    timestamp_pubnub = time.time()
    decrypted_message = decrypt(received_messsage.message)
    message = decrypted_message['message'].lower()
    speaker = decrypted_message['speaker'].lower()
    timestamp_start = decrypted_message['timestamp_start']
    timestamp_speaker = decrypted_message['timestamp_speaker']
    timestamp_text = decrypted_message['timestamp_text']

    timestamp_stop = time.time()
    light_control(message, speaker)

    speaker_reco_dur = timestamp_speaker - timestamp_start
    text_reco_dur = timestamp_text - timestamp_speaker
    cloud_dur = timestamp_pubnub - timestamp_text
    acturation_dur = timestamp_stop - timestamp_pubnub
    total_dur = sum([speaker_reco_dur, text_reco_dur, cloud_dur, acturation_dur])
    with open('output.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([speaker, message, round(speaker_reco_dur, 3), round(text_reco_dur, 3), round(cloud_dur, 3), round(acturation_dur, 3), round(total_dur, 3)])
