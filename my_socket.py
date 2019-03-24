import threading, sys, socket
from connection import Connection
from msgtype import MsgType

class ListeningThread(threading.Thread):
	#Listens to incoming connections
	def __init__(self, socket, connections, lock):
		threading.Thread.__init__(self)
		self.socket = socket
		self.connections = connections
		self.lock = lock
	def run(self):
		try:
			self.socket.listen(1)
			while True:
				con, client_address = self.socket.accept()
				AcceptingThread(Connection(con), self.connections, self.lock).start()
		finally:
			print("Api socket error")

class AcceptingThread(threading.Thread):
	#Waits for users to authenticate themselves
	def __init__(self, connection, connections, lock):
		threading.Thread.__init__(self)
		self.connections = connections
		self.connection = connection
		self.lock = lock
	def run(self):
		#Wait for username
		data = self.connection.receive_map()
		if data['type'] == MsgType.AUTH:
			try:
				self.lock.acquire()
				self.connections[data['username']] = self.connection
			finally:
				self.lock.release()
		else:
			print('rejecting connection %s' % data)

class Socket:
	def __init__(self, socket_address):
		self.connected_users = {}
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print(sys.stderr, 'binding socket on %s port %s' % socket_address)
		sock.bind(socket_address)
		ListeningThread(sock, self.connected_users, threading.Lock()).start()

	def send_new_message_alert(self, username):
		try:
			print('connected users: ' + str(self.connected_users))
			con = self.connected_users.get(username)
			if con:
				alert_map = {'type': MsgType.ALERT}
				con.send_map(alert_map)
		except Exception as e:
			print('error sending message alert' + str(e))