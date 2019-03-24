import socket
import sys
import json
from connection import Connection
from msgtype import MsgType
import requests

class Client:
    def __init__(self, socket_address, api_address, username):
        self.socket_address = socket_address
        self.api_address = api_address
        self.username = username

    def socket_connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(sys.stderr, 'connecting to socket %s port %s' % self.socket_address)
        sock.connect(self.socket_address)
        self.connection = Connection(sock)

    def authenticate(self, username):
        auth_map = {'type': MsgType.AUTH, 'username': username}
        self.connection.send_map(auth_map)

    def send_message(self, to_user, message):
        return requests.post("http://localhost:5000/send_message",  json={'from_user': self.username, 'to_user': to_user, 'message': message})

    def load_messages(self, from_time):
        return requests.get("http://localhost:5000/load_messages",  json={'username': self.username, 'from_time': from_time})

    def wait_for_alert(self):
        data = self.connection.receive_map()
        if data['type'] == MsgType.ALERT:
            return 0


    def socket_close(self):
        self.connection.close()