#!/Users/ben/anaconda/bin/python

from CharacterAttsHelper import getAttributes, getFixedAttributes
from CategoryAttsHelper import getSuperCategories
from language_generator import generate_riddle
from perception import extract_properties_from_perception
from TwitterSender import sendTweet
import random
from noc import parse, NOC
import time
import cPickle
from codecs import open
import os 
from sys import exit

random.seed()

# Load logbook
try:
	log = open('logbook.txt','a','utf8')
except:
	log = open('logbook.txt','w','utf8')

# Load list of latest 50 used characters
try:
	latest_50 = cPickle.load(open('latest_50.txt','r'))
except:
	latest_50 = [''] * 50
	
noc = parse(NOC)
names = []
for elem in noc[1:]:
	name = elem["Character"]
	if name not in latest_50:
		names.append(name)


NE = random.choice(names)
#NE = 'Jay Leno'
latest_50.pop(0)
latest_50.append(NE)
#assert len(latest_50) == 50
cPickle.dump(latest_50,open('latest_50.txt','w'))

print NE

properties = getSuperCategories(NE)
#print properties
perception_props = extract_properties_from_perception(NE)
if perception_props:
	#print "USING PERCEPTION"
	for p in perception_props:
		properties[p].extend(perception_props[p])
#print properties
fixed_attrs = getFixedAttributes(NE)
#print fixed_attrs

riddle = generate_riddle(properties, NE, fixed_props=fixed_attrs)

# Make sure the riddles are not longer than 140 characters to fit in a tweet
if not riddle:
	os.system('python theriddlerbot.py')
	exit()
while len(riddle) > 140:
	riddle = generate_riddle(properties, NE, fixed_props=fixed_attrs)

#print riddle
#print
sendTweet(riddle)

log.write(time.ctime()+u'\n'+NE+u'\n'+riddle+u'\n\n')
log.close()