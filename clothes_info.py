from collections import defaultdict
from noc import parse

#File employed to retrieve the determiners
clothesFile = "Veale's clothing line.xlsx"
clothesContent = parse(clothesFile)

"""
Function employed to obtain the determiner associated to the given clothes.
If the clothes does not exist inside the file for this purpose, the result is None.
@param clothes a String with the name of the clothes
@return A string with the determiner for the given clothes, or None
"""
def get_clothes_determiner(clothes):
    for c in clothesContent:
        if c["Clothing"].lower() == clothes.lower():
            return c["Determiner"]
    return None

"""
For testing purposes only
"""
if __name__ == "__main__":
    print get_clothes_determiner("apron")
