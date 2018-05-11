from mongo_connect import connectMongo
import constants
import pymongo
import json
from pprint import pprint
from init import init

collection = connectMongo()

##### WQ1 #####

init()
print('\nWQ1\n')

print('Initially:')
table = collection.find()
for data in table:
	pprint(data)
	print

print('\nAfter adding:\n')

with open('dummy-fitness.json') as json_file:
	json_object = json.load(json_file)

for data in json_object:
	collection.insert(data)

table = collection.find()
for data in table:
	pprint(data)
	print


##### WQ2 #####

print('\nWQ2\n')

print('\nInitially:')
table = collection.find()
for data in table:
	pprint(data)
	print

# print('\nAfter adding:')

with open('user1001-new.json') as json_file:
	js = json.load(json_file)

for field in js:
	collection.update({ 'uid': js['uid'] }, { '$set': {field: js[field]} } )

table = collection.find()
for data in table:
	pprint(data)
	print


##### RQ1 #####

print('\nRQ1\n')
print("Total number of employees whose data is in the AggieFit database: " + str(collection.count()))
print

##### RQ2 #####

print('\nRQ2\n')
table = collection.find()
result = []
print('UID of employees who have active tag')
for user in table:
	tags = user['tags']
	if ('active' in tags):
		result.append(user['uid'])

pprint(result)
print

##### RQ3 #####

print('\nRQ3\n')
table = collection.find()
result = []
print('UID of employees that have a goal step count greater than 5000 steps.')
for user in table:
	goalStep = user['goal']['stepGoal']
	if (goalStep > 5000):
		result.append(user['uid'])

pprint(result)
print

##### RQ4 #####

print('\nRQ4\n')
table = collection.find()
result = {}
print('UID and aggregation total activity duration for each employee')
for user in table:
	if ('activityDuration' not in user):
		result[user['uid']] = 0
	else:
		result[user['uid']] = sum(user['activityDuration'])

pprint(result)
print









