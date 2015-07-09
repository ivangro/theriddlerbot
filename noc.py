#!/Users/ben/anaconda/bin/python

try:
	from pattern.db import pd
except:
	import os
	import inspect
	def pd(*args):
		""" Returns the path to the parent directory of the script that calls pd() + given relative path.
			For example, in this script: pd("..") => /usr/local/lib/python2.x/site-packages/pattern/db/..
		"""
		f = inspect.currentframe()
		f = inspect.getouterframes(f)[1][1]
		f = f != "<stdin>" and f or os.getcwd()
		return os.path.join(os.path.dirname(os.path.realpath(f)), *args)


CELLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def xlsx(path):
    
    import zipfile
    from xml.etree.ElementTree import iterparse
    a = []
    r = {}
    v = ""
    z = zipfile.ZipFile(path)
    s = [e.text for x, e in iterparse(z.open("xl/sharedStrings.xml")) if e.tag.endswith("}t")]
    for x, e in iterparse(z.open("xl/worksheets/sheet1.xml")):
        if e.tag.endswith("}v"): # <v>84</v>
            v = e.text
        if e.tag.endswith("}c") \
         and e.attrib.get("t"):  # <c r="A3" t="s"><v>84</v></c>
            v = s[int(v)]
        if e.tag.endswith("}c"):
            c = e.attrib["r"]    # AZ22
            c = c.rstrip("0123456789")
            r[c], v = v, ""
        if e.tag.endswith("}row"):
            if any(r.values()):  # skip empty rows
                a.append(r)
            r = {}
    m = max([max(r.keys()) for r in a])
    for i, r in enumerate(a):    # fill empty cells
        for c in CELLS.split(m)[0] + m:
            r.setdefault(c, "")
        a[i] = [r[c] for c in sorted(r)]
    return a
    
    
def assoc(rows):
    """ Returns an iterator of rows, where each row is a dict of (header, value)-items.
    """
    headers = rows[0]
    for r in rows[1:]:
        r = dict((headers[i], v) for i, v in enumerate(r))
        yield r
        


def col(rows, key):
    """ Returns an iterator of values in the given column.
        For a list of lists, the given key is a number (index).
        For a list of dicts, the given key is a string.
    """
    for r in rows:
        yield r[key]

def split(v, separator=","):
    """ Returns the given string as a list.
    """
    return [x.strip() for x in v.split(separator)]

#print split("funny, entertaining", ",") # ["funny", "entertaining"]

def splitable(col, separator=",", threshold=1):
    """ Returns True if (some of) the values are strings that contain the separator.
    """
    i = 0
    for v in col:
        if isinstance(v, basestring) and separator in v:
            i += 1
        if i >= threshold:
            return True
    return False

def index(rows, key, unique=True):
    """ Returns a dict of (value for key, row)-items.
        With unique=False, returns a dict of (value for key, [row1, row2, ...])-items.
    """
    m = {}
    for r in rows:
        k = r[key]
        if not isinstance(k, list):
            k = [k]
        for k in k:
            if not unique:
                m.setdefault(k, []).append(r)
            else:
                m[k] = r
    return m

#rows = [["Daniel", "m"], ["Tina", "f"], ["Abraham", "m"]]
#print index(rows, 1, unique=False) # {"m": [["Daniel", "m"], ["Abraham", "m"]], 
                                    #  "f": [["Tina", "f"]]}

def freq(col, top=10):
    """ Returns a sorted list of (count, value)-tuples for values in the given list.
        The list is truncated to the top most frequent values.
    """
    f = {}
    for v in col:
        if not isinstance(v, list):
            v = [v]
        for v in v:
            if v not in f:
                f[v] = 0
            f[v] += 1
    f = f.items()
    f = sorted(((count, v) for v, count in f), reverse=True)
    return f[:top]

# ------------------------------------------------------------------------------------

def parse(path):
    # 1) Parse the Excel sheet at the given path (xlsx()).
    # 2) Map the list of lists to list of dicts (assoc()).
    # 3) If a column contains splitable values (e.g., "1,2,3"),
    # 4) split the values in the column.
    rows = list(assoc(xlsx(pd(path)))) # 1 + 2
    for k in rows[0].keys():
        if splitable(col(rows, k)):    # 3
            for r in rows:
                r[k] = split(r[k])     # 4
    return rows

        
NOC = "Veale's The NOC List.xlsx"            

#print parse(NOC)
    