#!/Users/ben/anaconda/bin/python

import random
from pattern.en import conjugate, referenced, parse
from pattern.db import Datasheet
from CharacterFinder import getCharactersWithTwoAttsInCommon, getCharacterWithFictionalWorld, getCharactersWithGroupAffiliation
from codecs import open

random.seed()

# Dictionary that contains transliterations of the different relationships
data = Datasheet.load('paraphrases.tsv',separator='\t',headers=False)
transliterations = {}
for c in data.columns:
	head = c[0]
	values = [w for w in c[1:] if w]
	transliterations[head] = values

# Dictionary with properties for testing purposes
test_props = {
"IS_A":['actor','comedian'],
"OPPONENT":['John Wilkes Booth'],
"CLOTHES":['a tweed jacket','pants','a stove-pipe hat']
}

fixed_props = {
'GENDER': ['male']}

# Possible beginnings of the riddle
introductions = [
('Tell me the name of a person that','3sg'),
("We're looking for a person who",'3sg'),
("I","1sg"),
("Who","3sg")
]


adjectival = ['NEGATIVE_PROPERTIES','POSITIVE_PROPERTIES','HAS_ATTRIBUTE']

def fw_analogy(character):
	fw_dict = getCharacterWithFictionalWorld(character)
	if not fw_dict:
		return None
	if len(fw_dict['Fictional Worlds']) == 0 or not fw_dict['Fictional Worlds'][0]:
		return None	
	fw1 = random.choice(fw_dict['Fictional Worlds'])
	if len(fw_dict['Results']) == 0 or not fw_dict['Results'][0]:
		return None	
	char2, fw2 = random.choice(fw_dict['Results'])
	scheme = random.choice(transliterations['FW_ANALOGY'])
	phrase = scheme.replace('OBJ1',fw1)
	phrase = phrase.replace('OBJ2',char2)
	phrase = phrase.replace('OBJ3',fw2)
	return phrase

def ga_analogy(character):
	ga_dict = getCharactersWithGroupAffiliation(character)
	if not ga_dict:
		return None
	if len(ga_dict['GroupAffiliation']) == 0 or not ga_dict['GroupAffiliation'][0]:
		return None
	ga1 = random.choice(ga_dict['GroupAffiliation'])
	if len(ga_dict['Results']) == 0 or not ga_dict['Results'][0]:
		return None
	char2, ga2 = random.choice(ga_dict['Results'])
	scheme = random.choice(transliterations['GA_ANALOGY'])
	phrase = scheme.replace('OBJ1',ga1)
	phrase = phrase.replace('OBJ2',char2)
	phrase = phrase.replace('OBJ3',ga2)
	return phrase
	
def generate_riddle(properties,character,fixed_props=None):
	"""
	Function that generates a riddle from a dictionary of properties.
	This dictionary contains key-value pairs where the key is the relationship with the NE
	and the value is a list containing all possible attributes.
	The 'fixed_props' parameter can contain a dictionary with elements we always want 
	to include in the riddle, such as GENDER or FICTIONAL_STATUS.
	"""
	
	# Select three properties and pick a random transliteration 
	# and an object from the dictionaries
	keys = properties.keys()
	random.shuffle(keys)
	elements = {}
	n = 0
	x = 0
	
	adjectives = []
	for tag in adjectival:
		if tag in properties:
			adjectives.extend(properties[tag])
	#print adjectives
	
	safety = []
	while x < 3+n and x < len(keys):
		safety.append(x)
		if len(safety) > 10:
			return None
		prop = keys[x]
		#if prop in adjectival and any([a in elements for a in adjectival]):
		#	n += 1
		#	x += 1
		#	continue
		if not prop in ['OPPONENT','CLOTHES','IS_A','TYPICAL_ACTIVITY','VEHICLE','COUNTRY','FICTIONAL_WORLD','GROUP_AFFILIATION']:
			n += 1
			x += 1
			continue
		if prop == 'FICTIONAL_WORLD':
			saying = fw_analogy(character)
			if not saying:
				continue
			object = None
			#print 'FW'
		elif prop == 'GROUP_AFFILIATION':
			saying = ga_analogy(character)
			if not saying:
				continue
			object = None
			#print 'GA'
		else: 
			saying = random.choice(transliterations[prop])
			object = random.choice(properties[prop])
		#words = saying.split(' ')
		if 'ADJP' in saying and 'ADJN' in saying:
			if 'POSITIVE_PROPERTIES' in properties and 'NEGATIVE_PROPERTIES' in properties:
				pass
			else:
				n += 1
				x += 1
				continue
		elements[prop] = (saying, object)
		x += 1
	
	riddle = ""
	intro,pers_nr = random.choice(introductions)
	riddle += intro
	if 'a person' in riddle:
		if fixed_props and 'IS_A' in elements:
			noun = fixed_props['GENDER'][0]
			if not any(['ADJ' in elem for elem in elements['IS_A']]):
				noun = random.choice(adjectives) + ' ' + noun
			riddle = riddle.replace('a person',referenced(noun))
	first = True
	for elem in elements:
		if first:
			first = False
		else:
			riddle += ','
		saying,object = elements[elem]
		#print saying, '//', object
		verbs = []
		for w in saying.split(' '):
			if w.endswith('/VB'):
				verbs.append(w)
		verbs = set(verbs)
		if len(verbs) > 0:
			for verb in verbs:
				saying = saying.replace(verb, conjugate(verb.split('/')[0],pers_nr))
		if elem == 'IS_A':
			if not 'ADJ OBJ' in saying:
				saying = saying.replace('OBJ',referenced(object))
			else:
				saying = saying.replace('OBJ',object)
		elif 'OBJ' not in saying:
			pass
		else:
			#print object
			saying = saying.replace('OBJ',object)
		if any([w in saying for w in ['ADJ','ADJN','ADJP']]):
			if 'NEGATIVE_PROPERTIES' in properties and 'POSITIVE_PROPERTIES' in properties:
				saying = saying.replace('ADJN',random.choice(properties['NEGATIVE_PROPERTIES']))
				saying = saying.replace('ADJP',random.choice(properties['POSITIVE_PROPERTIES']))
			saying = saying.replace('ADJ ',referenced(random.choice(adjectives))+' ')	

		riddle += " " + saying
	if riddle.startswith('Who '):
		riddle += '?'
	else:
		riddle += '.'
	if riddle.startswith('I '):
		riddle += random.choice([' Who am I?',' Who might I be?'])
	if riddle.startswith('There '):
		riddle += ' Who is this?'
	return riddle
	
if __name__ == "__main__":
	print generate_riddle(test_props,'The Joker')
	print fw_analogy('The Joker')
	print ga_analogy('Osama Bin Laden')


	