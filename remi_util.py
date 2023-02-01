import os

def read_data(fileName):
	file = open("data/"+fileName,"r")
	text = file.read()
	file.close()
	return text

def write_data(fileName,data):
	path = "temp/"+fileName
	with open(path,"wb") as f:
		f.write(data)
	return path

def fileExists(string):
	return os.path.exists(string)
