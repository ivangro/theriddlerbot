#!/Users/ben/anaconda/bin/python

from pattern.db import Datasheet, flip
from collections import defaultdict
from pattern.en import referenced

code_rel = {
'is-part-of_REVERSE':'HAS_PART',
'is-property-of_REVERSE':'HAS_PROPERTY',
'is-a':'IS_A'
}

# Load the commonsense database from Perception (nodebox.net/perception)
perception = Datasheet.load('commonsense.csv',header=False)

# Make a list of all the nodes
entities = flip(perception)[0]
entities.extend(flip(perception)[2])

# Gather the edges per node
graph = defaultdict(list)
for p in perception:
	graph[p[0]].append((None,p[1],p[2]))
	graph[p[2]].append((p[0],p[1],None))

def extract_properties_from_perception(NE):
	"""
	Extracts properties of persons/characters (here: NE) from the Perception database
	"""
	# First check if the NE occurs in the database at all
	if NE in entities:
		properties = defaultdict(list)
		# Select all properties of the NE from perception ('graph')
		elements = graph[NE]
		# For each property in perception, add a relationship and object to the output dictionary
		for e in elements:
			relationship = e[1]
			# In perception, relationships can work in two ways, so check both options
			if e[0]:
				relationship += "_REVERSE"
				object = e[0]
			else:
				object = e[2]
			try:
				relationship = code_rel[relationship]
				properties[relationship].append(object)
			except:
				pass
		return properties
	else:
		return None

if __name__ == "__main__":
	print extract_properties_from_perception('Ronald McDonald')
