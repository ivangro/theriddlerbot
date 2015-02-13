#!/Users/ben/anaconda/bin/python

from twitter_interaction import send_tweet
from database_handler import load_database
from pattern.db import Datasheet
import random
import sys

# Load database
db = load_database('theriddlerbot')

# Load possible answer phrasings
answers = Datasheet.load('answer_paraphrases.tsv',headers=True,separator='\t')

# Select last tweeted riddle
id,tweet,time,NE,status,favorites,retweets = db.riddles.rows()[-1]

if not status:
	# Randomly select an answer paraphrase
	if tweet.startswith('I '):
		answer = random.choice(answers[:,1])
	else:
		answer = random.choice(answers[:,0])
	text = answer.replace('NE',NE)
	print text
	# Post the answer as reply to the original riddle tweet
	send_tweet(text,reply_id=id)
	db.riddles.update(id, status=True)