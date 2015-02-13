from collections import defaultdict
from noc import parse,  col
from DeterminersHelper import getClothesDeterminer

nocFile = "Veale's The NOC List.xlsx"
#print "Loading file...",  nocFile
nocContent = parse(nocFile) #assoc(xlsx(nocFile))
#print "Loading ",  nocFile,  " done"

determiners = ("Seen Wearing")

columns = {"Category": "IS_A", 
                    "Typical Activity": "TYPICAL_ACTIVITY",  
                    "Seen Wearing": "CLOTHES", 
                    "Negative Talking Points":"NEGATIVE_PROPERTIES", 
                    "Positive Talking Points":"POSITIVE_PROPERTIES",
                    "Fictive Status":  "FICTIONAL_STATUS", 
                    "Gender": "GENDER", 
                    "Group Affiliation": "GROUP_AFFILIATION",
                    "Fictional World":"FICTIONAL_WORLD",
                    "Address 3": "COUNTRY"}
                    
fixedAttsColumns = {"Fictive Status": "FICTIONAL_STATUS",  "Gender": "GENDER"}

#Obtains a set of characters that share one of the given values for the given attribute
#@param values is a dictionary where the key is one of the columns and the value is a list of values for the attribute
def getCharactersFromValues(values):
    #print "Received values ",  values
    chars = set()
    #Get every attribute inside the list
    for att in values:
        #Get every value associated to the attribute
        for value in values[att]:
            #print "Looking for attribute value ",  value
            #For every possible value look the characters that share it
            for c in getCharacterList():
                vals = getAttributes(c)
                #Looking values of c inside vals
                if vals is not None:
                    #print "Looking inside ",  vals,  " from ",  c
                    for v in vals [att]:
                        if value == v.lower():
                            #print "Value found",  value,  " for character ",  c
                            chars.add(c)
    return chars
    
#Obtains a dictionary with the attribute values for the given character
#   {"IS_A": value, "CLOTHES": value, ...}
#@param characterName
    #If the value is empty doesn't include it

#Obtains a dictionary with all the possible attributes for the given character
def getAllAttributes(characterName):
    dict = defaultdict(list)
    #nocContent = assoc(xlsx(nocFile))
    for row in nocContent:
        if row["Character"] == characterName:
            for attrib in row:
                if len(row[attrib]) > 0:
                    #print "Values for ",  attrib ,  ": ",  row[attrib]
                    if isinstance(row[attrib],  list):
                        for val in row[attrib]:
                            if val:
                                dict[attrib].append(val)
                    else:
                        dict[attrib].append(row[attrib])
            return dict
            
def getAttributes(characterName):
    dict = defaultdict(list)
    #nocContent = assoc(xlsx(nocFile))
    for row in nocContent:
        if row["Character"] == characterName:
            for attrib in row:
                if attrib in defaultdict.keys(columns)  and attrib not in defaultdict.keys(fixedAttsColumns):
                    if len(row[attrib]) > 0:
                        #print "Values for ",  attrib,  ": ",  row[attrib]
                        if attrib == "Category":
                            for val in row[attrib]:
                                dict[columns[attrib]].append(val.lower())
                        elif attrib in determiners:
                            for val in row[attrib]:
                                if len(val) > 0:
                                    det = getClothesDeterminer(val)
                                    if not det:
                                        dict[columns[attrib]].append(val)
                                    else:
                                        dict[columns[attrib]].append(det + " " + val)
                        else:
                            for val in row[attrib]:
                                if len(val) > 0:
                                    dict[columns[attrib]].append(val)
            return dict

#Obtains the fixed attributes' values for the given character
#@param characterName
    #fictional_status, gender
def getFixedAttributes(characterName):
    dict = defaultdict(list)
    #nocContent = assoc(xlsx(nocFile))
    for row in nocContent:
        if row["Character"] == characterName:
            for attrib in row:
                if attrib in defaultdict.keys(fixedAttsColumns):
                    #print "Values for ",  attrib,  ": ",  row[attrib]
                    if attrib == "Gender":
                        if row[attrib] == "male":
                            val = "man"
                        elif row[attrib] == "female":
                            val = "woman"
                        dict[columns[attrib]].append(val)
                    else:
                        dict[columns[attrib]].append(row[attrib])
            return dict
    
#Translates the excel's column name to the name that we're internally using
def getColumnName(excelName):
    return columns[excelName]

#Obtains a list with all the character names
def getCharacterList():
    try:
        #nocContent = parse(nocFile)
        return list(col(nocContent,  "Character"))
    except Exception as e:
        print e

#Testing
if __name__ == "__main__":
    #print getCharacterList()
    print getAttributes("Albert Einstein")
#    print getFixedAttributes("Albert Einstein")
    #print getAttributes("Tina Fey")
#    attsSet = set()
#    attsSet.add("academic")
#    attsSet.add("problem solver")
#    attsSet.add("intellectual")
#    attsSet.add("smart person")
#    print getCharactersFromValues({"IS_A": attsSet})
    print getAllAttributes("Albert Einstein")
