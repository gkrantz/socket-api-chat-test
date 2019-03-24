import json

class Connection:
	def __init__(self, connection):
		self.connection = connection

	def send_map(self, object):
		if self.connection:
			self.connection.sendall(json.dumps(object).encode())
		else:
			print('No connection')

	def receive_map(self):
		if self.connection:
			data = self.connection.recv(4096)
			if data:
				return json.loads(data)
			else:
				return ""
		else:
			print('No connection')

	def close(self):
		self.connection.close()