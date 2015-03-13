#!/Users/ben/anaconda/bin/python

from CharacterAttsHelper import getAttributes, getFixedAttributes
from CategoryAttsHelper import getSuperCategories
from language_generator import generate_riddle
from perception import extract_properties_from_perception
from twitter_interaction import send_tweet
from database_handler import load_database, insert_riddle
import random
from noc import parse, NOC
import time
import cPickle
from codecs import open
import os 
from sys import exit

random.seed()

db = load_database('theriddlerbot')

# Load list of latest 50 used characters
try:
	latest_50 = cPickle.load(open('latest_50.txt','r'))
except:
	latest_50 = [''] * 50
	
# Load names of characters from NOC list	
noc = parse(NOC)
names = []
for elem in noc[1:]:
	name = elem["Character"]
	if name not in latest_50:
		names.append(name)

def riddlerbot():
	"""
	Outputs riddle about character randomly picked from NOC list.
	Properties of the character are extracted from NOC list and Perception.
	The properties are bundled into a riddle by the language generator.
	"""
	
	# Pick a random character from the list
	# If the character was one of the last 50 to be used, pick another one
	# Update and save the list of last 50 characters
	NE = random.choice(names)
	while NE in latest_50:
		NE = random.choice(names)
	latest_50.pop(0)
	latest_50.append(NE)
	#assert len(latest_50) == 50
	cPickle.dump(latest_50,open('latest_50.txt','w'))
	#print NE

	# Retrieve properties from the character from the NOC list and Perception
	# Put them together in one dictionary
	properties = getSuperCategories(NE)
	perception_props = extract_properties_from_perception(NE)
	if perception_props:
		for p in perception_props:
			properties[p].extend(perception_props[p])
	fixed_attrs = getFixedAttributes(NE)

	riddle = generate_riddle(properties, NE, fixed_props=fixed_attrs)


	return riddle,NE

for x in range(1):
	riddle = None
	# Make sure the riddles are not longer than 140 characters to fit in a tweet
	while not riddle or len(riddle) > 140 or riddle in db.riddles.filter('text'):
		riddle,NE = riddlerbot()

	if riddle:
		#print riddle
		#print
		post_id,timestamp = send_tweet(riddle)
		insert_riddle(db,post_id,riddle,NE,timestamp)
	else:
		print 'no riddle posted'
