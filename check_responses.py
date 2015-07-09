#!/Users/ben/anaconda/bin/python

from twitter_interaction import send_tweet, get_replies, add_friend, get_friends, favorite
from database_handler import load_database, update_score, insert_response, load_paraphrases
from pattern.db import Datasheet, date, ALL
from wikipedia_utils import find_aliases
import random
import sys
import time

db = load_database('theriddlerbot')

templates = load_paraphrases()

# Load the last posted riddle from the database
try:
	last_tweet = db.riddles.rows()[-1]
except:
	print "Cannot load last tweet"
	sys.exit()

# Don't bother checking for replies if the riddle has already been solved
if last_tweet[4]:
	print "Riddle already solved"
	sys.exit()

# If there is one, load the last seen response from the database
try:
	last_answer = db.responses.rows()[-1]
except:
	last_answer = last_tweet

# Get all new responses to this riddle from Twitter
replies = get_replies(last_tweet[0], since=last_answer[0])

correct = last_tweet[3]
# Add aliases from wikipedia redirects
aliases = find_aliases(correct)
correct_expanded = {x.lower():1 for x in aliases}

# Go through the responses chronologically
for item in sorted(replies.keys()):
	post_id, author_id, author_name, text, timestamp = replies[item]
	# Ignore own posts
	if author_name == 'TheRiddlerBot':
		continue
	if author_id not in get_friends():
		userdata = add_friend(author_id)
	text = text.lower().strip('\'\"-,.:;!?')
	#print author_name, author_id, text, timestamp
	
	if text.strip() in correct_expanded:
		# Tweet that it was correct
		tw = '.@'+author_name+' '+random.choice(templates['RESP_CORRECT']).replace('NE',correct)
		#print tw
		send_tweet(tw, reply_id=post_id)
		favorite(post_id)
		# Update user score
		update_score(db,author_id,author_name)
		# Change status of riddle to solved and add nr of responses before the correct answer
		db.riddles.update(last_tweet[0], {'status':True,'nr_responses':db.responses.count()}) 
		break
	else:
		# Tweet that it wasn't correct
		tw = '@'+author_name+' '+random.choice(templates['RESP_INCORRECT'])
		#print tw
		send_tweet(tw, reply_id=post_id)
		# Insert response in database
		insert_response(db,post_id,author_id,author_name,text,timestamp)
		continue
	
#print replies