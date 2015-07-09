#!/Users/ben/anaconda/bin/python

from pattern.web import URL, Twitter
from pattern.db import date
import json
from keyholder import riddlerbot_key

def jload(url):
	"""Execute twitter assignment in url and download/read its data with json."""
	return json.loads(url.open().read())

def send_tweet(tweet, reply_id=False, reply_user=None):
	"""
	Send tweets from our twitter account: @TheRiddlerBot
	Parameter 'tweet' is a string with the message to be sent
	Optional parameters (for replying to tweets)
		'reply_id' is the id of the message to answer to.
		'reply_user' is the user of the original message, to use as mention
	Returns the tweet id if the message was successfully sent
	"""
	if reply_id:
		if reply_user:
			if not reply_user.startswith('@'):
				reply_user = '@' + reply_user
			tweet = reply_user + " " + tweet
		url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet, "in_reply_to_status_id": reply_id})
	else:
		url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet})
	twitter = Twitter(license=riddlerbot_key)
	url = twitter._authenticate(url)
	
	try:
		# Send the post request while downloading its data
		data = jload(url)
		post_id = int(data[u'id'])
		timestamp = date(data[u'created_at'])
		print "Message successfully sent: " + tweet
	except Exception as e:
		print e
		print e.src
		print e.src.read()
		return 0,date(0)
	return post_id,timestamp

def get_replies(reply_id, since=None):
	"""
	Retrieve all replies that were posted since the tweet with id 'since' 
	as a reply to the tweet with the 'reply_id'.
	Returns a dictionary with timestamps as keys and 
	tuples of user name and tweet text as values.
	"""	
	if not since:
		since = reply_id
	url = URL("https://api.twitter.com/1.1/statuses/mentions_timeline.json", method="get", query={"since_id":since})
	twitter = Twitter(license=riddlerbot_key)
	url = twitter._authenticate(url)
	
	user_replies = {}
	try:
		data = jload(url)
		for reply in data:
			if reply["in_reply_to_status_id"] == reply_id:
				#print reply
				post_id = reply["id"]
				author_name = reply["user"]["screen_name"].encode('utf-8')
				author_id = reply["user"]["id"]
				text = reply["text"].replace("@TheRiddlerBot","").strip()
				timestamp = date(reply["created_at"])
				user_replies[timestamp] = post_id,author_id,author_name,text,timestamp 
	except Exception as e:
		print e
		print e.src
		print e.src.read()
		return {}
	return user_replies

def get_stats(id):
	"""
	Retrieve the number of retweets and favorites of the tweet with the given id.
	"""
	url = URL("https://api.twitter.com/1.1/statuses/show.json", method="get", query={"id":id})
	twitter = Twitter(license=riddlerbot_key)
	url = twitter._authenticate(url)
	try:
		data = jload(url)
		#print data
	except Exception as e:
		print e
		return 0,0
	nr_retw = data['retweet_count']
	nr_fav = data['favorite_count']
	return nr_retw,nr_fav
	
def add_friend(user_id):
	"""
	Start following the account with given user id
	"""
	url = URL("https://api.twitter.com/1.1/friendships/create.json", method="post", query={"user_id": user_id, 'following': "true"})
	twitter = Twitter(license=riddlerbot_key)
	url = twitter._authenticate(url)
	print 'Friend added'
	return jload(url)
	
def get_friends():
	"""
	Retrieve all accounts we follow
	"""
	url = URL("https://api.twitter.com/1.1/friends/ids.json", method="get", query={"screen_name": "TheRiddlerBot"})
	twitter = Twitter(license=riddlerbot_key)
	url = twitter._authenticate(url)
	data = jload(url)
	return data[u"ids"]

def favorite(id):
	"""
	Favorite the tweet with given id
	"""
	url = URL("https://api.twitter.com/1.1/favorites/create.json", method="post", query={"id": id})
	twitter = Twitter(license=riddlerbot_key)
	url = twitter._authenticate(url)
	data = jload(url)
	return data

if __name__ == "__main__":
	#print get_stats(557089932356104192)
	#t = send_tweet('ok1')
	#print get_friends()
	print add_friend(424525840)