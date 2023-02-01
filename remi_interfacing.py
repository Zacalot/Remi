import requests
import whisper
import openai
import pyaudio
import wave
from subprocess import call
import urllib
from urllib.parse import urlencode
from win32 import win32clipboard
from io import BytesIO
from PIL import Image
import keyboard
import remi_util

openai.api_key = remi_util.read_data("openai_apikey")

# Advanced SST system
whispModel = whisper.load_model("base")

def play_tts(text):
	call(["espeak","-s140","-ven+f2",text])

def type_text(text):
	for char in text:
		keyboard.write(char)

def copy_image_file(filepath):
	image = Image.open(filepath)
	output = BytesIO()
	image.convert("RGB").save(output, "BMP")
	data = output.getvalue()[14:]
	output.close()
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardData(win32clipboard.CF_DIB,data)
	win32clipboard.CloseClipboard()

def get_audio_text(audio):
	result = whispModel.transcribe(remi_util.write_data("speech.wav",audio.get_wav_data()))
	return result["text"].strip()

def query_openai(prompt):
	response = openai.Completion.create(
		model="text-davinci-003",
		prompt=prompt,
		temperature=0,
		max_tokens=100,
		top_p=1.0,
		frequency_penalty=0.2,
		presence_penalty=0.0
	)
	
	if "choices" in response:
		if len(response["choices"]) > 0:
			answer = response["choices"][0]["text"]
	return answer.strip()

wolfram_appID = remi_util.read_data("wolfram_apikey")
def ask_wolfram(question):
	url = '&'.join(["http://api.wolframalpha.com/v1/spoken?appid="+wolfram_appID, urllib.parse.urlencode({'i': question})])
	try:
		response = urllib.request.urlopen(url)
		return response.read().decode("utf-8")
	except:
		return "No result for: "+question

p = pyaudio.PyAudio()
def play_wav(wav):
	f = wave.open(wav,"rb")
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
					channels = f.getnchannels(),
					rate = f.getframerate(),
					output = True)
	data = f.readframes(1024)
	while data:
		stream.write(data)
		data = f.readframes(1024)
	stream.close()
	f.close()

#----------MEMEGEN----------

def get_meme_templates():
	data = requests.get("https://api.imgflip.com/get_memes").json()["data"]["memes"]
	images = [{"name":image["name"],"url":image["url"],"id":image["id"]} for image in data]
	return images

imgflip_user = remi_util.read_data("imgflip_credentials").split("\n")[0]
imgflip_password = remi_util.read_data("imgflip_credentials").split("\n")[1]
def generate_meme(template,topText,bottomText):
	URL = "https://api.imgflip.com/caption_image"
	params = {
		"username":imgflip_user,
		"password":imgflip_password,
		"template_id": template,
		"text0": topText,
		"text1": bottomText
	}
	response = requests.request("POST",URL,params=params).json()
	print("GOT RESPONSE",response)
	opener = urllib.request.URLopener()
	opener.addheader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 \
    Safari/537.36")
	fileName, headers = opener.retrieve(response["data"]["url"], "temp/meme.jpg")
	return fileName
