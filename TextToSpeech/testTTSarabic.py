import wave
from piper.voice import PiperVoice

model2 = "/home/milan/E-SHARA/TextToSpeech/models/ar_JO-kareem-medium.onnx"
voice2 = PiperVoice.load(model2)
text2 = " مرحبا من فريق إشارة اضغط على الزر الاحمر للبدء"
wav_file2 = wave.open("output2.wav", "w")
audio2 = voice2.synthesize(text2, wav_file2)
