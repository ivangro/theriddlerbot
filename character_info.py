from collections import defaultdict
from noc import parse,  col
from clothes_info import get_clothes_determiner

nocFile = "Veale's The NOC List.xlsx"
#print "Loading file...",  nocFile
nocContent = parse(nocFile)
#print "Loading ",  nocFile,  " done"

"""
Mapping for the excel's colum names into our internal names
Excel's name -> Internal name
"""
columns = {"Category": "IS_A", 
                    "Typical Activity": "TYPICAL_ACTIVITY",  
                    "Seen Wearing": "CLOTHES", 
                    "Negative Talking Points":"NEGATIVE_PROPERTIES", 
                    "Positive Talking Points":"POSITIVE_PROPERTIES",
                    "Fictive Status":  "FICTIONAL_STATUS", 
                    "Gender": "GENDER", 
                    "Group Affiliation": "GROUP_AFFILIATION"}

"""
List of attributes that will include a determiner for each value.
Important: This determiners are found into different related files, and additional functions should be added for this purpose.
"""
determiners = ("Seen Wearing")

"""
Translates the excel's column name to the name that we're internally using
"""
def get_column_name(excelName):
    return columns[excelName]
    
"""
Obtains a dictionary with all the possible attributes for the given character
@param characterName A string representing the character name 
@param internalNames A If true, the internal name of the column replaces the excel's name
@return a dictionary which has as keys the column name and as value a list with the values for the attribute.
"""
def get_attributes(characterName,  internalNames):
    dict = defaultdict(list)
    #nocContent = assoc(xlsx(nocFile))
    for row in nocContent:
        if row["Character"] == characterName:
            for attrib in row:
                if len(row[attrib]) > 0:
                    #print "Values for ",  attrib ,  ": ",  row[attrib]
                    #Replace the name of the attribute with our internal name
                    if internalNames and attrib in columns: 
                        attribName = columns[attrib] 
                    else: 
                        attribName = attrib
                    #If the value is a list, add each element, otherwise add the value to the dictionary
                    if isinstance(row[attrib],  list):
                        for val in row[attrib]:
                            if val:
                                finalVal = _validate_value(val,  attrib)
                                dict[attribName].append(finalVal)
                    else:
                        finalVal = _validate_value(row[attrib],  attrib)
                        dict[attribName].append(finalVal)
            return dict

"""
Obtains a set of characters that share one of the given values for the given attribute
@param values is a dictionary where the key is one of the columns and the value is a list of values for the attribute
@return A set of characters that share the same given values
"""
def get_characters_by_values(values):
    chars = set()
    #Get every attribute inside the list
    for att in values:
        #Get every value associated to the attribute
        for value in values[att]:
            #print "Looking for attribute value ",  value
            #For every possible value look the characters that share it
            for c in _get_characters_list():
                vals = get_attributes(c,  True)
                #Looking values of c inside vals
                if vals is not None:
                    #print "Looking inside ",  vals,  " from ",  c
                    for v in vals [att]:
                        if value == v.lower():
                            #print "Value found",  value,  " for character ",  c
                            chars.add(c)
    return chars
    
"""
@return Obtains a list with all the character names
"""
def _get_characters_list():
    try:
        return list(col(nocContent,  "Character"))
    except Exception as e:
        print e

"""
Obtains the determiner for the given value and attribute name
@param value The value to look for its determiner
@param attributeName The excel's column name
@return A string with the determiner and the value, if the determiner exists
NOTE: This function also converts to lower case the category name
"""
def _validate_value(value,  attributeName):
    if attributeName in determiners:
        if attributeName == "Seen Wearing":
            det = get_clothes_determiner(value)
            if not det:
                return value
            else:
                return det + " " + value
    
    if attributeName == "Category":
        return value.lower()
    return value

#Testing
if __name__ == "__main__":
    print get_attributes("Albert Einstein",  True)["POSITIVE_PROPERTIES"]
    #print get_attributes("Anthony Bourdain",  True)
#    attsSet = set()
#    attsSet.add("academic")
#    attsSet.add("problem solver")
#    attsSet.add("intellectual")
#    attsSet.add("smart person")
#    print get_characters_by_values({"IS_A": attsSet})
