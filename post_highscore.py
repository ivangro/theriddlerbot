#!/Users/ben/anaconda/bin/python

from twitter_interaction import send_tweet
from database_handler import load_database, reset_week_scores
import operator
import time

# Load database
db = load_database('theriddlerbot')

week_scores = db.user_scores.filter(('author_name', 'correct_answers_week'))
week_scores = sorted(week_scores, key=operator.itemgetter(1), reverse=True)

top3 = []
rank = 1
for name,count in week_scores:
	if rank > 3:
		break	
	if count != 0:
		top3.append(str(rank)+'. @'+name+ ' ('+ str(count) +')')
		rank += 1

tweet = "This week's top scorers are: " + ', '.join(top3)
#print tweet
post_id,timestamp = send_tweet(tweet)

time.sleep(1800)

scores = db.user_scores.filter(('author_name','correct_answers'))
scores = sorted(scores, key=operator.itemgetter(1), reverse=True)

top3 = []
rank = 1
for name,count in scores:
	if rank > 3:
		break
	if count != 0:
		top3.append(str(rank)+'. @'+name+ ' ('+ str(count) +')')
		rank += 1

tweet = "The all-time best riddle-solvers are: " + ', '.join(top3)
#print tweet
post_id,timestamp = send_tweet(tweet)

db = reset_week_scores(db)
