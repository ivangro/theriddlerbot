from collections import defaultdict
from character_info import get_attributes,  get_characters_by_values,  _get_characters_list

"""
Looks for the name and group association of another character with the same category
    Must have group association
@param character The character name
@return  Obtains a dictionary with two keys:
    The first is "GroupAffiliation" which value is a list with the character's group affiliations.
    The second is "Results" which is a list of tuples in the form (character, group affiliation).
"""
def get_characters_by_group_affiliation(characterName):
    res = list()
    attributes = get_attributes(characterName,  False)
    groupAffiliations = attributes["Group Affiliation"]
    if len(groupAffiliations) > 0:
        #Look for characters that share the same group affiliation
        categories = attributes["Category"]
        attsSet = set()
        for category in categories:
            attsSet.add(category.lower())
        #print "Looking for similar categories ",  attsSet
        characterList = get_characters_by_values({"IS_A": attsSet})
        #print "Similar groups ",  characterList
        for c in characterList:
            groups = get_attributes(c,  False)["Group Affiliation"]
            for g in groups:
                if c <> characterName and g not in groupAffiliations:
                    res.append((c, g))
        
        return {"GroupAffiliation": groupAffiliations,  "Results":res}

"""
Looks for the name and fictional world of another character with the same category
    Must have fictional world
@param character The character name
@return Obtains a dictionary with two keys:
    The first is "FictionalWorlds" which value is a list with the character's fictional worlds.
    The second is "Results" which is a list of tuples in the form (character, fictional world).
"""
def get_characters_by_fictional_world(characterName):
    res = list()
    attributes = get_attributes(characterName,  False)
    isFictive = attributes["Fictive Status"]
    if len(isFictive) > 0:
        fictionalWorlds = attributes["Fictional World"]
        #Look for characters that share the same category
        attsSet = set()
        for category in attributes["Category"]:
            attsSet.add(category.lower())
        #print "Looking for similar categories ",  attsSet
        characterList = get_characters_by_values({"IS_A": attsSet})
        #print "Similar category ",  characterList
        for c in characterList:
            fictiveWorld = get_attributes(c,  False)["Fictional World"]
            for w in fictiveWorld:
                if c <> characterName and w not in fictionalWorlds:
                    res.append((c, w))
        
        return {"Fictional Worlds": fictionalWorlds,  "Results":res}

"""
Looks for characters that share values of the given types
@param character The character's name
@param attributesList A list with the internal attribute names to look for similar characters
@param COMMON_VALUES A number determining the minimum number of common attributes
@return Obtains a list of characters
"""
def get_characters_by_common_atts(characterName,  attributesList,  COMMON_VALUES):
    res = list()
    attributes = get_attributes(characterName,  True)
    attsDict = defaultdict(set)
    
    #Obtains all the character's values for the given attributes 
    for attribute in attributesList:
        attsSet = set()
        for value in attributes[attribute]:
            attsSet.add(value)
        attsDict[attribute] = attsSet
    
    #Look for similar characters
    characters = _get_characters_list()
    for c in characters:
        commonAtts = 0
        atts = get_attributes(c,  True)
        for attribute in attributesList:
            newSet = set()
            for value in atts[attribute]:
                newSet.add(value)
            
            intersect = attsDict[attribute].intersection(newSet)
            commonAtts = commonAtts + len(intersect)
        if commonAtts >= COMMON_VALUES and c <> characterName:
            res.append(c)
    
    return res

"""
For testing purposes
"""
if __name__ == "__main__":
    print get_characters_by_common_atts("Abraham Lincoln",  ("POSITIVE_PROPERTIES",  "NEGATIVE_PROPERTIES"),  2)
    print
#    print get_characters_by_fictional_world("The Joker")
#    print
#    print  get_characters_by_group_affiliation("Osama Bin Laden")
