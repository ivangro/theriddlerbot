from pattern.web import Wikipedia,  URL,  GET
import re

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
Obtains the aliases for the given character from his wikipedia page
@param characterName The name of the character
@return A list with all the character aliases
"""
def find_aliases(characterName):
    aliases = []
    article = Wikipedia().search(characterName.replace(' ', '_'))
    if article:
        title = article.title
        #print "Title found ",  title
        my_url = 'http://dispenser.homenet.org/~dispenser/cgi-bin/rdcheck.py?page='
        my_url = my_url + title.replace(' ',  '_')
        #print "Looking for ",  my_url
        contents = URL(my_url).download(user_agent='Mozilla/5.0').split('\n')
        headerFinder = '<h3><i class=\"nosections\">No anchor or section</i></h3>'
        aliasFinder = '<li><a href=\".*\">(.+)</a></li>'
        endHeaderFinder = '</ul>'
        headerFound = False
        for line in contents:
            if not headerFound:
                header = re.search(headerFinder,  line)
                if header:
                    headerFound = True
                    #print "Header found"
            else:
                endHeader = re.search(endHeaderFinder,  line)
                if not endHeader:
                    alias = re.search(aliasFinder,  line)
                    if alias:
                        #print "Group: ",  alias.groups(0)[0]
                        aliases.append(alias.groups(0)[0])
                else:
                    #print "End of header detected"
                    break
        #print "FINISHED"
    return aliases

"""
Looks in wikipedia the dates of birth and death for a given character
@param characterName The name of the character
@return A tuple with two dates (birth, death)
"""
def find_dates(characterName):
    article = Wikipedia().search(characterName.replace(' ', '_'))
    bday = None
    dday = None
    if article:
        contents = article.source
        bdayFinder = '<span class=\"bday\">(\d+-\d+-\d+)</span>'
        ddayFinder = '<span class=\"dday\s+deathdate\">(\d+-\d+-\d+)</span>'
        res = re.search(bdayFinder,  contents)
        if res:
            bday = res.groups(0)[0]
        res2 = re.search(ddayFinder,  contents)
        if res2:
            dday = res2.groups(0)[0]
        if bday or dday:
            return (bday,  dday)
    return ()            
    
"""
For testing purposes only
"""
if __name__ == "__main__":
#    props = ('inventive', 'imaginative', 'farseeing', 'clever', 'creative', 'brilliant', 'curious')
#    character = "Albert Einstein"
#    print "Looking ",  props ,  " in ",  character,   " wikipedia page"
#    print find_relevance(character,  {"POSITIVE_PROPERTIES": props})
    print find_aliases("The Riddler")
    print find_dates("Barak Obama")
