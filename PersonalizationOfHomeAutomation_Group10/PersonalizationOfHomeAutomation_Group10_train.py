print("Initializing the program...")

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import json
import torchaudio

def record_train_audio(user, duration=12, samplerate=16000):
    print("recording Training Clip...")
    # Channel 1 for mono recording
    voice_recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("finished recording.")
    file_path = f"train_{user}.wav"
    write(file_path, samplerate, voice_recording)
    return file_path

print("loading the model...")
from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.inference.ASR import EncoderDecoderASR
# Speaker Recognition Model ECAPA-TDNN 
speaker_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb", 
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)
# Speech Recognition Model Wav2Vec 2.0 
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-wav2vec2-commonvoice-en", 
    savedir="pretrained_models/asr-wav2vec2-commonvoice-en"
)
print("models are imported.")

try:
    while True:
        user = input('Type in your username: ')
        print(f"read following text (around 10 seconds): Hello, my name is {user}, and I am excited to explore the fascinating world of artificial intelligence. Let's discover new possibilities!")
        if input("Press 'ENTER' to start recording OR Press 'ANY KEY' then 'ENTER' to quite the program: ").lower() != '':
            print("Exiting the program")
            break

        train_audio = record_train_audio(user=user)
        print(f"{train_audio} is saved")

        signal, fs = torchaudio.load(train_audio)
        # Resample to 16000 Hz if not already
        if fs != 16000:
            resampler = torchaudio.transforms.Resample(fs, 16000)
            signal = resampler(signal)
        embedding = speaker_model.encode_batch(signal)
        # flatten the embedding to a a 1D array
        embedding = embedding.flatten().detach().cpu().numpy()
        # Save embeddings to disk
        embedding_path = f"embedding_{user}.npy"
        np.save(embedding_path, embedding)

        try:
            with open("user_profile.json", 'r') as file:
                user_profile = json.load(file)
        except FileNotFoundError:
            user_profile = {}

        user_profile[user] = embedding_path
        with open("user_profile.json", 'w') as file:
            json.dump(user_profile, file, indent=4)

        print(f"Training complete; {embedding_path} is saved, and user_profile.json is updated")

        if input("Press 'ENTER' to add additional user OR Press 'ANY KEY' then 'ENTER' to quit the program: ").lower() != '':
            print("Exiting the program")
            break

except KeyboardInterrupt:
    print("Exiting the program")
