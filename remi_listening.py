import audioop
import pyaudio
import numpy as np
import speech_recognition as sr
import deepspeech

KEYWORDS = ["remi","remy"]

LISTEN_DURATION = .5 # How long it listens before analyzing speech

CHUNK_SIZE = 1024
SAMPLE_RATE = 16000
FORMAT = pyaudio.paInt16

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
				channels=1,
				rate=SAMPLE_RATE,
				input=True,
				frames_per_buffer=CHUNK_SIZE)

SAMPLE_WIDTH = p.get_sample_size(FORMAT)
seconds_per_buffer = float(CHUNK_SIZE)/SAMPLE_RATE

LISTEN_SIZE = 50

# Quick and dirty SST for constant listening
model = deepspeech.Model("resources/deepspeech/deepspeech-0.9.1-models.pbmm")
model.enableExternalScorer("resources/deepspeech/deepspeech-0.9.1-models.scorer")
model.addHotWord("remi",float(10000))

stt = sr.Recognizer()

def listen_for_remi():
	recording_left = 0
	frames = []
	print("LISTENING")
	while True:
		buffer = stream.read(CHUNK_SIZE)
		frames.append(buffer)
		if len(frames) > LISTEN_SIZE:
			del frames[1]
		if recording_left <= 0:
			energy = audioop.rms(buffer,SAMPLE_WIDTH)
			if energy >= 700:
				recording_left = LISTEN_DURATION
		if recording_left > 0:
			recording_left -= seconds_per_buffer
			if recording_left <= 0:
				result = model.stt(np.frombuffer(b''.join(frames),np.int16))
				frames = []
				for v in KEYWORDS:
					if v in result:
						return True
