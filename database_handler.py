#!/Users/ben/anaconda/bin/python

from pattern.db import Database, field, pk, STRING, BOOLEAN, DATE, NOW, INTEGER, PRIMARY, ALL


def load_database(dbname):
	"""
	Load the database and the 'riddles' table. Creates either if not present.
	"""
	data = Database(dbname)
	
	if not 'riddles' in data.tables:
		print "Create new table: riddles"
		data.create('riddles',fields=(
		field('id', INTEGER, index=PRIMARY,optional=False),
		field('text', STRING(140), index=True,optional=False), 
		field('timestamp',DATE,index=True, default=NOW ),
		field('answer',STRING(140)),
		field('status', BOOLEAN, default=False ),
		field('favorites', INTEGER, default=0),
		field('retweets', INTEGER, default=0)
		))
	
	if not 'responses' in data.tables:
		print 'Create new table: responses'
		data.create('responses',fields=(
		field('id',INTEGER,index=PRIMARY,optional=False),
		field('answer',STRING(140),index=True, optional=False),
		field('evaluation',INTEGER,index=True, optional=False)
		))
	
	if not 'user_scores' in data.tables:
		print 'Create new table: user_scores'
		data.create('user_scores',fields=(
		field('profile_id',INTEGER,index=PRIMARY,optional=False ),
		field('name',STRING(30),index=True,optional=False ),
		field('correct_answers', INTEGER,optional=False, default=0)
		))
	
	return data

def insert_riddle(data,riddle):
	"""
	Inserts riddle information into the database's table of riddles
	"""
	data.riddles.append(id=riddle[0],text=riddle[1],answer=riddle[2])
	return data

def insert_response(data,response):
	"""
	Inserts response information into the database's table of responses to the current riddle
	"""
	data.responses.append(id=response[0],answer=response[1],evaluation=response[2])
	return data
	
def update_score(data,user):
	"""
	Updates or inserts user score into the database's table of user scores to the current riddle
	"""
	if user[0] in data.user_scores.filter('profile_id'):
		score = data.user_scores.filter('correct_answers', profile_id=user[0])
		data.user_scores.update(user[0],fields={'correct_answers':score+1})
	else:
		data.user_scores.append(profile_id=user[0],name=user[1],correct_answers=1)
	return data
	
if __name__ == '__main__':
	data = load_database('theriddlerbot')
	#data = insertRiddle(data,(12,'Help','ok'))
	print data.riddles
	print data.riddles.rows()
	#x = data.riddles.filter(ALL,id='12')
	#print x