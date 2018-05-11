from mongo_connect import connectMongo
import constants
import pymongo
import json

def init():
	'''
		This function initializes the database
	'''
	collection = connectMongo()
	collection.remove()
	print('Database reinitialized')