print("Initializing the program...")

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from cryptography.fernet import Fernet
import json
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import torchaudio
import time

def record_test_audio(duration=3, samplerate=16000):
    print("recording Commend...")
    # Changed channels 1 for mono recording
    voice_recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("finished recording.")
    file_path = f"voice_commend.wav"
    write(file_path, samplerate, voice_recording)
    return file_path

def recognize_speaker(test_wav_path):
    global saved_embeddings
    signal, fs = torchaudio.load(test_wav_path)
    # Resample to 16000 Hz if not already
    if fs != 16000:
        resampler = torchaudio.transforms.Resample(fs, 16000)
        signal = resampler(signal)
    
    test_embedding = speaker_model.encode_batch(signal)
    # flatten the embedding to a a 1D array
    test_embedding = test_embedding.flatten().detach().cpu().numpy()

    # Compare with saved embeddings using cosine similarity
    similarities = {}
    for user, saved_embedding in saved_embeddings.items():
        similarity = np.dot(saved_embedding, test_embedding) / (np.linalg.norm(saved_embedding) * np.linalg.norm(test_embedding))
        similarities[user] = similarity
        print(f"{user}: {similarity*100:.2f}%")

    # Determine the most likely speaker based on similarity scores
    recognized_user = max(similarities, key=similarities.get)
    return recognized_user, similarities[recognized_user]

def encrypt(data_in_dict):
    global hard_coded_key
    data_bytes = json.dumps(data_in_dict).encode('utf-8')
    cipher = Fernet(hard_coded_key)
    encrypted_data = cipher.encrypt(data_bytes).decode('utf-8')
    return encrypted_data

def publish_to_pubnub(publish_key, subscribe_key, channel_name, user_id, data):
    pnconfig = PNConfiguration()
    pnconfig.publish_key = publish_key
    pnconfig.subscribe_key = subscribe_key
    pnconfig.user_id = user_id

    pubnub = PubNub(pnconfig)

    channel_name = channel_name

    def publish_callback(result, status):
        if status.is_error():
            print(status.status_code, status.error_data.__dict__)
        else:
            print(f"message is sent successfully, timetoken: {result.timetoken}")

    pubnub.subscribe().channels(channel_name).execute()
    pubnub.publish().channel(channel_name).message(data).pn_async(publish_callback)
    pubnub.stop()


from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.inference.ASR import EncoderDecoderASR
print('loading model...')
# Speaker Recognition Model
speaker_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb", 
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)
# Speech Recognition Model
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-wav2vec2-commonvoice-en", 
    savedir="pretrained_models/asr-wav2vec2-commonvoice-en"
)

with open('user_profile.json', 'r') as file:
    user_profile = json.load(file)

saved_embeddings = {user: np.load(f"embedding_{user}.npy") for user in user_profile.keys()}

hard_coded_key = b'gkmrxaiQZVDTGKl1Cqv_3to8ZqhJ6wQFzGt6uoeRfRk='

try:
    while True:
        if input("Press 'ENTER' to start recording OR Press 'ANY KEY' then 'ENTER' to quite the program: ").lower() != '':
            print("Exiting the program")
            break
        voice_commend = record_test_audio()
        timestamp_start = time.time()
        speaker, score = recognize_speaker(voice_commend)
        timestamp_speaker = time.time()
        text = asr_model.transcribe_file(voice_commend)
        timestamp_text = time.time()
        print(f"speaker: {speaker}\nmessage: {text}")

        data = {
            'speaker': speaker,
            'message': text,
            'timestamp_start': timestamp_start,
            'timestamp_speaker': timestamp_speaker,
            'timestamp_text': timestamp_text
        }

        encrypted_data = encrypt(data)

        publish_key = "pub-c-f564a900-4f5e-48df-8e24-5580aa48cf59"
        subscribe_key = "sub-c-76a8dc4d-28dc-4468-ba6b-9f4ab714a7a3"
        channel_name = "Channel-Barcelona"
        user_id = "minhao"
        publish_to_pubnub(publish_key,subscribe_key, channel_name, user_id, encrypted_data)
        time.sleep(1)

        if input("Press 'ENTER' to record next commend OR Press 'ANY KEY' then 'ENTER' to quit the program: ").lower() != '':
            print("Exiting the program")
            break
        
except KeyboardInterrupt:
    print("Exiting the program.")
