from collections import defaultdict
from noc import parse,  split
from CharacterAttsHelper import getAttributes,  getColumnName,  getCharactersFromValues

def loadContent():
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
catContent = loadContent()
#catContent = parse(categoryFile)
#print catContent
#print "Loading ",  categoryFile,  " done"

#Obtains a set with all the available attributes for the given character including its super categories
#@param characterName
def getSuperCategories(characterName):
    superCategories = list()

    #Obtain the category of a character
    atts = getAttributes(characterName)
    category = atts[getColumnName("Category")]
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
    
#Obtains all the available characters that share a super category with the given character
#@param characterName
def getCharacterBySuperCategories(characterName):
    categoriesFound = set()
    superCategories = getSuperCategories(characterName)["SUPER_CATEGORY"]
    #Look for categories that belong to one of the found super categories
    for row in catContent:
        #print "Looking for categories with super category ",  row
        for elem in row["Super Category"]:
            if elem.lower() in superCategories: #and elem.lower() not in category:
                for cat in row["Category"]:
                    categoriesFound.add(cat.lower())
                    #print "Category added ",  cat.lower()
    
    #print "Categories found: ",  categoriesFound
    #Look for the characters that belong to one of the categories found
    characters = getCharactersFromValues({"IS_A":categoriesFound})
    return characters

def retrieveValues(attribute,  key):
    values = defaultdict(list)
    try:
        nocContent = parse(categoryFile)
        for val in freq(col(nocContent,  attribute)):
            if len(val[1]) > 0:
                values[key].append(val[1])
        return values
    except Exception as e:
        print e

#column = "Super Category"
#print retrieveValues("Super Category",  "SC")
if __name__ == "__main__":
    charac = "Albert Einstein"
    print "Looking super categories of ",  charac
    print getSuperCategories(charac)
#    print "Looking similar characters of ",  charac
#    print getCharacterBySuperCategories(charac)
