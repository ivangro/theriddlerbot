#!/Users/ben/anaconda/bin/python

from pattern.db import Database, field, pk, STRING, BOOLEAN, DATE, NOW, INTEGER, PRIMARY, ALL
from codecs import open

def load_database(dbname):
	"""
	Load the database and the 'riddles' table. Creates either if not present.
	"""
	data = Database(dbname)
	
	if not 'riddles' in data.tables:
		print "Create new table: riddles"
		data.create('riddles',fields=(
		field('post_id', INTEGER, index=PRIMARY,optional=False),# id of the tweet containing the riddle
		field('text', STRING(140), index=True,optional=False),	# the text of the riddle
		field('timestamp',DATE,index=True, default=NOW ),		# the time the riddle tweet was sent
		field('answer',STRING(140)),							# the correct answer to the riddle
		field('status', BOOLEAN, default=False ),				# has the riddle been solved or answered?
		field('favorites', INTEGER, default=0),					# nr of favorites of the riddle tweet
		field('retweets', INTEGER, default=0),					# nr of retweets of the riddle tweet
		field('nr_responses', INTEGER, default=0)				# nr of responses to the riddle tweet
		))
	
	if not 'responses' in data.tables:
		print 'Create new table: responses'
		data.create('responses',fields=(
		field('post_id',INTEGER,index=PRIMARY,optional=False),		# id of response tweet
		field('timestamp',DATE,index=True, default=NOW ),			# the time the response was sent
		field('author_id',INTEGER,optional=False ),					# id of author of response
		field('author_name',STRING(30),optional=False ),			# name of author of response
		field('response',STRING(140), optional=False),				# the posted response
		))
	
	if not 'user_scores' in data.tables:
		print 'Create new table: user_scores'
		data.create('user_scores',fields=(
		field('author_id',INTEGER,index=PRIMARY,optional=False ),	# id of twitter user
		field('author_name',STRING(30),index=True,optional=False ),		# name of twitter user
		field('correct_answers', INTEGER,optional=False, default=0)	# nr of correct answers
		))
		
	return data

def insert_riddle(data,post_id,text,answer,timestamp):
	"""
	Inserts riddle information into the database's table of riddles
	"""
	data.riddles.append(post_id=post_id,text=text,answer=answer,timestamp=timestamp)
	return data

def insert_response(data,post_id,author_id,author_name,response,timestamp):
	"""
	Inserts response information into the database's table of responses to the current riddle
	"""
	data.responses.append(post_id=post_id,author_id=author_id,author_name=author_name,response=response,timestamp=timestamp)
	return data
	
def update_score(data,author_id,author_name):
	"""
	Updates or inserts user score into the database's table of user scores to the current riddle
	"""
	if author_id in {row[0]:True for row in data.user_scores.filter('author_id')}:
		score = data.user_scores.filter('correct_answers', author_id=author_id)[0][0]
		score += 1
		data.user_scores.update(author_id,correct_answers=score)
	else:
		data.user_scores.append(author_id=author_id,author_name=author_name,correct_answers=1)
	return data
	
def load_paraphrases():
	"""
	Loads possible paraphrases for both riddle and answer creation
	Returns a dictionary with different categories of paraphrases as keys
	"""
	paraphrases = {}
	tmp = open('phrase_templates.tsv','r','utf8')
	lines = tmp.readlines()
	tmp.close()
	for line in lines:
		line = line.strip().split('\t')
		paraphrases[line[0]] = line[1:]
	return paraphrases
	
if __name__ == '__main__':
	data = load_database('theriddlerbot')
	#data = insertRiddle(data,(12,'Help','ok'))
	#print data.riddles
	#print data.riddles.rows()
	#x = data.riddles.filter(ALL,id='12')
	#print x
	#print load_paraphrases()
	#update_score(data,2,'ben')
	#print data.user_scores.rows()
