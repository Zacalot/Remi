import os
import re
import sys
sys.path.insert(0, os.getcwd().replace("\\","/")) #Fixes an issue where I can't import local files

import remi_util
import remi_commands
from remi_commands import *

funcs = {}
for func in dir(remi_commands):
	if func[0:2] != "__":
		func_attr = getattr(remi_commands,func)
		if callable(func_attr):
			funcs[func] = func_attr.__doc__

gpt3_template = """Convert text a programmatic command.
Only produce commands including the following of this list:"""
for func in funcs:
	gpt3_template += "\n- "+func

gpt3_template += "\n\nConvert text into these commands based on the following examples:"

for func in funcs:
	gpt3_template += "\n"+funcs[func]

gpt3_template += "\n%s"

from remi_interfacing import *
import remi_listening
import speech_recognition as sr

def say(text,noSave=False):
	print(": "+text)
	play_tts(text)

def beep():
	play_wav("resources/sfx/beep.wav")

def boop():
	play_wav("resources/sfx/boop.wav")

def execute_commands(commands):
	func_name = commands
	if func_name:
		code = commands
		res = eval(code)
		if res:
			remi_commands.lastSpoke = res
			return res
	else:
		return "Sorry, command failed."
	return "Command executed."

def execute_query(query):
	print("Executing query: "+query)
	try:
		func_call = query_openai(gpt3_template % query).strip()
		print("Calling: "+func_call+"\n")
		reply = execute_commands(func_call)
		say(reply)
	except Exception as e:
		print("Failed to execute: "+query)
		print("Error: "+e.message if hasattr(e,"message") else e)
		say("Error.")

while True:
	if remi_listening.listen_for_remi(): # Heard 'remi' trigger
		beep()
		with sr.Microphone() as source:
			audio = remi_listening.stt.listen(source) #Record audio until silence
			boop()
			voice_command = get_audio_text(audio)
			execute_query(voice_command)
			boop()
