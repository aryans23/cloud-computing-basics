import redis
dir(redis)

from mongo_connect import connectMongo
import constants
import pymongo
from pprint import pprint
from init import init

r = redis.Redis()
collection = connectMongo()

### 
# Uncomment the below line to re-initialize the database whenever the script is called
# init()
###

subscribing = False;		# to denote if this application is subscribing to anyone
board = -1;					# to mark which message_board it's pointing to currently
message_board = ""			# The string name of the message_board

while True:
	try:
		if subscribing:
			print("Subscribing to " + str(message_board))
			for item in p.listen():	
				print(item)

		cmd = raw_input('Enter your command: ')
		# print(cmd)
		cmd_parts = cmd.split(" ")
		# print(cmd_parts)
		
		if (cmd_parts[0] == "quit" or cmd_parts[0] == "q"):
			break;
		
		elif cmd_parts[0] == "select":		# select a message_board
			if (cmd_parts[1] == ""):
				print("Error: select needs a message board, Please select a message board")
				continue
			if (cmd_parts[1] == "health_quotes"):
				r = 0;
				message_board = "health_quotes"
				print("Message Board health_quotes selected!")
			elif (cmd_parts[1] == "fit_chat"):
				board = 1;
				message_board = "fit_chat"
				print("Message Board fit_chat selected!")
			else:
				print("Error: No such message board exists")

		elif cmd_parts[0] == "read":		# display every logged messages
			if (board == -1):
				print("Error: select needs a message board, Please select a message board")
				continue
			table = collection.find({"mb" : board})
			for data in table:
				pprint(data["quote"])

		elif cmd_parts[0] == "write":		# write the message
			if (board == -1):
				print("Error: select needs a message board, Please select a message board")
				continue
			if (cmd_parts[1] == ""):
				print("Error: No message to write")
				continue
			to_write = ' '.join(cmd_parts[1:])
			collection.insert({"mb": board, "quote": to_write})		# write to database
			res = r.publish(message_board, to_write) 		# publish
			print res

		elif cmd_parts[0] == "listen":			# listen to the current channel
			if (board == -1):
				print("Error: select needs a message board, Please select a message board")
				continue
			subscribing = True;
			p = r.pubsub()
			res = p.subscribe(message_board) 
			if res is not None:
				print(res[data])

		else:
			if (cmd_parts[0] != ""):
				print("Input format wrong");

	except KeyboardInterrupt:
		subscribing = False
		print