from pattern.web import Wikipedia

"""
Looks for the given attribute values at the wikipedia page of the character
@param characterName The name of the character
@param attributes A dictionary which key is an attribute name and the value associated is a list of values for the attribute
@return A dictionary which key is the attribute name and the value associated is a decimal value that determines the ratio 
    between the values found inside the wikipedia page of the character and the total values of the attribute
"""
def find_relevance(characterName,  attributes):
    article = Wikipedia().search(characterName)
    contents = article.string
    #print "Page found ",  len(contents) > 0
    
    results = {}
    for att in attributes:
        #print "Looking values for ",  att
        attributesFound = 0
        for value in attributes[att]:
            if value in contents:
                attributesFound += 1
                #print "Value found: ",  value
        if attributesFound > 0 and len(attributes[att]) > 0:
            results[att] = attributesFound * 1.0 / len(attributes[att])
            #print "Found: ",  attributesFound,  " Total: ",  len(attributes[att])
        #print "Values found in wikipedia for attribute ",  att,  ": ",  attributesFound
        
    return results

"""
For testing purposes only
"""
if __name__ == "__main__":
    props = ('inventive', 'imaginative', 'farseeing', 'clever', 'creative', 'brilliant', 'curious')
    character = "Albert Einstein"
    print "Looking ",  props ,  " in ",  character,   " wikipedia page"
    print find_relevance(character,  {"POSITIVE_PROPERTIES": props})
