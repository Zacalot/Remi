import xmlrpc.client
import remi_util

server_ip = remi_util.read_data("discordserver").split("\n")[0]
server_port = int(remi_util.read_data("discordserver").split("\n")[1])

def get_server_proxy():
	return xmlrpc.client.ServerProxy("http://%s:%s/" % (ip,port))

def send_announcement(msg):
	with get_server_proxy() as proxy:
		proxy.announce(msg)

def upload_file(path):
	with open(path,"rb") as handle:
		binary_data = xmlrpc.client.Binary(handle.read())
		with get_server_proxy() as proxy:
			return proxy.upload_file("image.png",binary_data)
