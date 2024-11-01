from speechbrain.inference.speaker import SpeakerRecognition
from speechbrain.inference.ASR import EncoderDecoderASR
print('loading model...')
# Speaker Recognition Model
speaker_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb", 
    savedir="pretrained_models/spkrec-ecapa-voxceleb"
)
# ASR Model
asr_model = EncoderDecoderASR.from_hparams(
    source="speechbrain/asr-wav2vec2-commonvoice-en", 
    savedir="pretrained_models/asr-wav2vec2-commonvoice-en"
)