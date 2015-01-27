from collections import defaultdict
from noc import parse,  split
from character_info import get_attributes,  get_column_name,  get_characters_by_values

"""
Loads the csv file contents to retrieve information related to the diferent categories of the characters
"""
def _load_content():
    i=0
    columns = {}
    for elem in split(catContentCSV.readline(),  "\t"):
        columns[str(i)] = elem
        i = i+1
    #print "Columns ",  columns

    content = list()
    line = catContentCSV.readline()
    while line:
        dict = defaultdict(list)
        i = 0
        for value in split(line,  "\t"):
            if len(value) > 0:
                dict[columns[str(i)]].append(value)
                i= i+1
        content.append(dict)
        line = catContentCSV.readline()
        
    return content

categoryFile = "Veale's category hierarchy.csv"
#print "Loading... ",  categoryFile
catContentCSV = open(categoryFile,  'r')
catContent = _load_content()
#print "Loading ",  categoryFile,  " done"

"""
Obtains a set with all the available attributes for the given character INCLUDING its super categories
@param characterName The name of the character
@return a dictionary which has as keys the column name and as value a list with the values for the attribute.
"""
def get_all_attributes(characterName):
    superCategories = list()

    #Obtain the category of a character
    atts = get_attributes(characterName,  True)
    category = atts[get_column_name("Category")]
    #print "Categories of the character: ",  category
    
    #Look for super categories
    for row in catContent :
        #print "Looking inside ",  row
        for cat in row["Category"] :
            if cat.lower() in category:
                #print "Category found ",  cat
                #Obtain the super categories
                for superCat in row["Super Category"]:
                    if len(superCat) > 0 and superCat.lower() not in superCategories:
                        #print "Super cat found ",  superCat,  " from ",  cat
                        superCategories.append(superCat.lower())    
    
    atts["IS_A"].extend(superCategories)
    return atts
    
"""
Obtains all the available characters that share a super category with the given character
@param characterName The name of the character
"""
def get_character_by_super_categories(characterName):
    categoriesFound = set()
    superCategories = get_all_attributes(characterName)[get_column_name("Category")]
    #Look for categories that belong to one of the found super categories
    for row in catContent:
        #print "Looking for categories with super category ",  row
        for elem in row["Super Category"]:
            if elem.lower() in superCategories: #and elem.lower() not in category:
                for cat in row["Category"]:
                    categoriesFound.add(cat.lower())
                    #print "Category added ",  cat.lower()
    
    #Look for the characters that belong to one of the categories found
    characters = get_characters_by_values({"IS_A":categoriesFound})
    return characters

"""
For testing
"""
if __name__ == "__main__":
    charac = "Albert Einstein"
    print "Looking super categories of ",  charac
    print get_all_attributes(charac)
    print "Looking similar characters of ",  charac
    print get_character_by_super_categories(charac)
