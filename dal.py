import pymongo
import time

class DAL:
	def __init__(self):
		myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		db = myclient["messageapp"]
		self.users = db["users"]
		self.messages = db["messages"]

	def add_user(self, username):
		self.users.insert({'username': username})

	def get_user(self, username):
		result = self.users.find_one({'username': username})
		if not result:
			self.add_user(username)
			return self.get_user(username)
		return result

	def get_user_byid(self, _id):
		result = self.users.find_one({'_id': _id})
		if not result:
			return None
		return result

	def get_messages(self, username, from_time):
		user = self.get_user(username)
		print('getting messages for user: %s' % user)
		result = list(self.messages.find({'to_user': user['_id'], 'time': {"$gt": from_time}}))
		return result

	def save_message(self, from_user, to_user, message):
		f_user = self.get_user(from_user)
		t_user = self.get_user(to_user)
		return self.messages.insert({'from_user': f_user['_id'], 'to_user': t_user['_id'], 'message': message, 'time': int(round(time.time() * 1000))})