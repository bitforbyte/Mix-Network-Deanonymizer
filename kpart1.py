#!/usr/bin/python3
import string
import sys
import ast

# Batch to hold the values from each batch
class Batch:
	def __init__(self, senders, recievers):
		self.senders = senders						# Those who sent messages
		self.recievers = recievers					# Those who recieved messages

class User:
	def __init__(self, name):
		self.name = name
		self.vecV = []		# Vector V: Sum of n=0 -> Infinity (n * Pm(n)) where n is number of messages sent by user. Pm is a probability function
		self.vecU = []		# Vector U: Background distribution: t' of batches user didn't send message( each batch i, construct vector ui, elements are 1/b for reveivers else 0)
		self.vecO =	[]		# Vector o: Rounds Alice sent message, the number of messages mi, sent
		self.tPrime = 0		# t'
		self.t = 0			# t
		self.bigO = 0		# Arithmetic mean of large set vecO
		self.bigU = 0		# Arithmetic mean of large set vecU

	# Process each of the batches to construct each of the vectors
	def Process(self, batches):
		pass
	

if __name__== "__main__":

	numUsers = 260		# N recipients
	numBatch = 32		# b for batch size

	users = []
	userDict = {}
	userDictV = {}
	for i in range(0, 26):
		letter = dict(zip(range(0, 26), string.ascii_lowercase))	
		for j in range(0, 10):
			letterName = letter[i] + string.digits[j]	# Get the letter names (a-z)(0-9)
			users.append(User(letterName))				# Users list that will hold each of the users in a class
			userDictV[letterName] = 1/2					# V is probability to send to each recipient (1/2 for two friends)
			userDict[letterName] = 0					# assign the dictionary for the U and V default values
	
	# Copy the dictionary into each of the dictionaries
	for user in users:
		user.vecV = userDictV.copy()
		user.vecU = userDict.copy()
		user.vecO = userDict.copy()
		
		

	# Read in the batches into a list
	# List to hold each batch
	batches = []
	lines = sys.stdin.readlines()	# Holds the raw input text

	numBatch = 0	# number of batches used for index (used for debug printing)
	
	# Loop through lines by 2 for S and R pairs
	for i in range(0, len(lines)-1,2):

		# Trim the sender and reciever lists to obtain a list of names
		sendersList = ast.literal_eval(lines[i][2:])		
		recieversList = ast.literal_eval(lines[i+1][2:])

		# assign the Senders and Recievers into the batch list
		batches.append(Batch(sendersList, recieversList))

		#print(rounds[numBatch].senders)
		#print(rounds[numBatch].recievers)

		# Increment index by one to use correct placement
		numBatch+=1
		
	# At this point we have all rounds with who spoke in each round
	# Calculate the messages send and not sent by each user
	# Not sent
	for user in users:
		# Traverse each batch to determine values for users
		for batch in batches:

			# If the user hasn't sent a message
			if user.name not in batch.senders:

				# Increment t' (number of batches not spoken in)
				user.tPrime += 1

				# Scan the recievers and set value to probability of message send (1/(Batch Size))
				for receivers in batch.recievers:
					user.vecU[receivers] = 1/numBatch	# numBatch(b) = 32

			else:	
				# User has sent a message in this batch
				# Increment t (number of batches spoken in)
				user.t += 1

				# TODO not sure if this is correct
				for receivers in batch.recievers:
					user.vecO[receivers] = 1/numBatch	# numBatch(b) = 32

		# Batches have been scanned
		# Calculate the big O and U using the Arithmetic mean
		if user.tPrime != 0:
			user.bigU = (1/user.tPrime) * (sum(user.vecU.values()))

		if user.t != 0:
			user.bigO = (1/user.t) * (sum(user.vecO.values()))

		print(user.name)
		#print(user.bigU)
		#print(user.bigO)
		
		# Assign the vector V (Final Formula)
		for val in user.vecV:
			user.vecV[val] = user.vecV[val] * ((32 * user.bigO) - (32 - 1)* user.bigU)
			print(user.vecV[val])
