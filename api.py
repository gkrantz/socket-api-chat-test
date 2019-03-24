import threading, sys
from msgtype import MsgType
from flask import Flask, request, jsonify
from my_socket import Socket
from dal import DAL
from bson import json_util

class APIServer:
	def __init__(self, socket_address, api_address):
		socket = Socket(socket_address)

		print(sys.stderr, 'Starting api server on %s port %s' % api_address)
		api = Flask(__name__)
		dal = DAL()

		@api.route('/')
		def index():
			return str(dal.get_user("shintaro"))

		@api.route('/send_message/', methods=["POST"])
		def send_message():
			if not request.json:
				abort(400)
			print(request.json)
			dal.save_message(request.json['from_user'], request.json['to_user'], request.json['message'])
			socket.send_new_message_alert(request.json['to_user'])
			return "ok"

		@api.route('/load_messages', methods=["GET"])
		def load_messages():
			if not request.json:
				abort(400)
			print('loading messages for %s' % request.json)
			result = dal.get_messages(request.json['username'], request.json['from_time'])
			print('returning %s' % result)
			return json_util.dumps(result)

		api.run()