#!/Users/ben/anaconda/bin/python

from twitter_interaction import send_tweet
from database_handler import load_database, load_paraphrases
from pattern.db import Datasheet, ALL
import random
import time
import cPickle

# Load database
db = load_database('theriddlerbot')

# Load possible answer phrasings
templates = load_paraphrases()

# Select last tweeted riddle
id,tweet,time,NE,status,favorites,retweets,nr_resp = db.riddles.rows()[-1]

if not status:
	# Randomly select an answer paraphrase
	if tweet.startswith('I '):
		answer = random.choice(templates['ANSW_1SG'])
	else:
		answer = random.choice(templates['ANSW_3SG'])
	text = '.@TheRiddlerBot ' + answer.replace('NE',NE)
	# Post the answer as reply to the original riddle tweet
	send_tweet(text,reply_id=id)
	db.riddles.update(id, {'nr_responses':db.responses.count()})
	db.responses.remove(ALL)
	# Indicate that answer has now been posted
	cPickle.dump(True, open('answer_posted.cPickle','w'))
else:
	print "The last riddle was already answered."

