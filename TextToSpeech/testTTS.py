import wave
from piper.voice import PiperVoice

model = "/home/milan/E-SHARA/TextToSpeech/models/en_US-lessac-high.onnx"
voice = PiperVoice.load(model)
text = "Hello from Eshara team ! My name is Razan."
wav_file = wave.open("output.wav", "w")
audio = voice.synthesize(text, wav_file)
