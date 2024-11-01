Package Required:
pip install sounddevice
pip install scipy
pip install cryptography
pip install pubnub
pip install torch torchaudio
pip install soundfile
pip install speechbrain
pip install transformers

Package Required for Pi:
pip install Rpi.GPIO
pip install cryptography
pip install pubnub

1. run personalization_of_home_automation_group10_model_download.py to download pretrained models.
2. run personalization_of_home_automation_group10_train.py to add user and voice.
3. run personalization_of_home_automation_group10_command.py to issue the commend

To establish cloud communication using PubNub, ensure you have a PubNub account. Please correctly configure followings in  the command.py and pi.py
- publish_key
- subscribe_key
- user_id
- channel_name
verify that the PubNub Access Manager is disabled.