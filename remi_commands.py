import remi_util
import remi_discord
import remi_interfacing
import pyperclip

lastSpoke = ""

def send_discord_message(msg):
	"""Tell my discord that I will be on in 30 minutes
send_discord_message("I will be on in 30 minutes")
Send a message to the discord server saying good morning everyone!
send_discord_message("good morning everyone!")

Send my clipboard to my discord
send_discord_message(get_clipboard())

Generate a meme of Iron Man with my clipboard as the top and bottom text, then send it to my Discord server.
send_discord_message(gen_meme("ironman", get_clipboard(), get_clipboard()))"""
	if remi_util.fileExists(msg):
		remi_discord.upload_file(msg)
		return "Successfully uploaded: "+msg
	else:
		remi_discord.send_announcement(msg)
		return "Successfully said: "+msg

def gen_meme(template,top_text,bottom_text):
	"""Make a meme of the guy pressing two buttons with the top text reading press the button and the bottom text reading don't press it
gen_meme("Two Buttons","Press the button","Don't press it")"""
	possible_memes = remi_interfacing.get_meme_templates()
	memeListTemplate = "Given the string '"+template+"' pick the entry from this list it closest describes:"
	for meme in possible_memes:
		memeListTemplate += '\n- '+meme["name"]
	memeListTemplate += "\nAnswer: "
	print("MEME LIST:")
	print(memeListTemplate)
	chosenTemplate = remi_interfacing.query_openai(memeListTemplate).strip('"')
	memeID = None
	for meme in possible_memes:
		if meme["name"] == chosenTemplate:
			memeID = meme["id"]
	if not memeID:
		return "No meme template found called: "+chosenTemplate
	return remi_interfacing.generate_meme(memeID,top_text,bottom_text)

def get_clipboard():
	"""Get my clipboard
get_clipboard()"""
	return pyperclip.paste()

def get_last_speech():
	"""Get what you last said
get_last_speech()
Tell me what you last said
get_last_speech()
Repeat what you just said
get_last_speech()
Send what you last said to discord
send_discord_message(get_last_speech())"""
	return lastSpoke

def set_clipboard(obj):
	"""Copy flowers are nice to my clipboard
set_clipboard("flowers are nice")
Look up the circumference of the Earth then copy it to my clipboard
set_clipboard(lookup_information("the circumference of the Earth"))"""
	if remi_util.fileExists(obj):
		remi_interfacing.copy_image_file(obj)
	else:
		pyperclip.copy(obj)

def type_text(text):
	"""Type out hello my friends
type_text("hello my friends")
Type out the depth of the mariana trench
type_text(lookup_information("the depth of the mariana trench"))"""
	remi_interfacing.type_text(text)
	return "Typed: "+text


def lookup_information(query):
	"""Lookup the height of mount everest
lookup_information("height of mount everest")
What is the square root of 9
lookup_information("the square root of 9")"""
	return remi_interfacing.ask_wolfram(query)

