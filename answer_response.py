#!/Users/ben/anaconda/bin/python

from twitter_interaction import send_tweet
from database_handler import load_database, load_paraphrases
from pattern.db import Datasheet, ALL
import random
import time

time.sleep(30)

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
	#db.riddles.update(id, status=True)
else:
	print "The last riddle was already answered."

db.responses.remove(ALL)