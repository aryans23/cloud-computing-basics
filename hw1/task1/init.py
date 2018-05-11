from mongo_connect import connectMongo
import constants
import pymongo
import json

def init():
	collection = connectMongo()
	collection.remove()

	with open('initial.json') as json_file:
		json_object = json.load(json_file)

	for data in json_object:
		collection.insert(data)

	print('Database reinitialized')