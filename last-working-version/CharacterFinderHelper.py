from collections import defaultdict
from noc import index,  parse,  assoc,  pd,  xlsx,  split
from CharacterAttsHelper import getColumnName,  nocFile

#Obtains a defaultdict which key is the value of one of the attributes displayed below from the given character
#   and the value is a list with the characters that share the same attribute value inside the excel file
#@param characterName The name of the character
#@param attribute One of the attribute names from the below list
#----------------------------------- Possible values for attribute --------------------------------------------------
# Character, Gender, Address 1, Address 2, Address 3, Politics, Marital Status, 
# Opponent, Typical Activity, Vehicle of Choice, Weapon of Choice, Seen Wearing,
# Domains, Genres, Fictive Status, Portrayed By, Creator, Creation, Group Affiliation,
# Fictional World, Category, Negative Talking Points, Positive Talking Points
def findCharacters(characterName,  attribute):
    values = defaultdict(list)
    
    try:
        res = list(assoc(xlsx(pd(nocFile))))
        for v in res:
            #Look for the attributes of the given character
            if v["Character"] == characterName:
                    value = v[attribute]
                    valueList = split(value) #Obtain the values of the given attribute
                    break
        
        #Look for characters with the same attribute's value 
        nocContent = parse(nocFile)
        for r in nocContent:
            for v in r[attribute]:
                for v2 in valueList:
                    if v == v2:
                        values[attribute].append(r["Character"])
                        break
                        
        return values
    except Exception as e:
        print e

#Testing
if __name__ == "__main__":
#    print findCharacters("Buck Rogers",  "Category")
#    print findCharacters("Doc Emmett Brown",  "Category")
    print findCharacters("Abraham Lincoln",  "Positive Talking Points")
