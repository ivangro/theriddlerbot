from collections import defaultdict
from noc import parse

clothesFile = "Veale's clothing line.xlsx"
#print "Loading... ",  categoryFile
clothesContent = parse(clothesFile)
#print "Loading ",  clothesFile,  " done"

def getClothesDeterminer(cloth):
    for c in clothesContent:
        if c["Clothing"] == cloth:
            return c["Determiner"]

if __name__ == "__main__":
    print getClothesDeterminer("apron")
