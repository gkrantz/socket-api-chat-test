from client import Client
import sys, json
import threading
from datetime import datetime

def load_and_print(username, from_time, hack):
	response = cli.load_messages(from_time)
	print('response: ' + str(response))
	list = json.loads(response.text)
	for item in list:
		print('[%s] %s: %s' % (datetime.fromtimestamp(item['time']/1000).strftime('%H:%M'), hack, item['message']))
	if len(list) > 0:
		return list[-1]['time']
	return 0

class ListeningThread(threading.Thread):
	#Listens to incoming connections
	def __init__(self, username, hack):
		threading.Thread.__init__(self)
		self.username = username
		self.hack = hack
	def run(self):
		try:
			last_message_time = -1
			while True:
				last_message_time = load_and_print(self.username, last_message_time, self.hack)
				cli.wait_for_alert()
		finally:
			print("Api socket error")

username = input("Username: ")
to_user = input("Chat with: ")		
print("Logging in %s..." % username)
cli = Client(('localhost', 10000), ('localhost', 5000), username)

try:
	cli.socket_connect()
	cli.authenticate(username)
	print("Logged in %s!" % username)

	ListeningThread(username, to_user).start()

	while True:
		message = input("")
		cli.send_message(to_user, message)

finally:
	cli.socket_close()