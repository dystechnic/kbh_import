import xml.etree.ElementTree as ET
import sqlite3
import sys

conn = sqlite3.connect('kb_daten.sqlite')
print('Connected to database successfully.')
cur = conn.cursor()
print("\n [+] Cursor has been set up successfully")

#filename = "hops.xml"
filename = sys.argv[-1]
tree = ET.parse(filename)
root = tree.getroot()

"""
Fields in hopfen table <==>   Fields in BeerXML Hops
Name                   <==>   NAME (text)
Menge                  <==>   INVENTORY (float)
Alpha                  <==>   ALPHA (float)
Pellets                <==>   FORM (1 = Pellet, 0 = Leaf) (integer)
Typ                    <==>   TYPE (1 = Aroma, 2 = Bittering, 3 = Both) (Integer)
Bemerkung              <==>   Origin (text)
Eigenschaften          <==>   NOTES (text)
Alternativen           <==>   SUBSTITUTES (text)
Preis
Eingelagert              
Mindesthaltbar
Link
"""
for member in root.findall('HOP'):
    name = member.find('NAME')
    if name is not None:
        name = member.find('NAME').text
    else:
        name = ""
    print(name)
    inventstr = member.find('INVENTORY')
    if inventstr is not None:
        inventstr = member.find('INVENTORY').text
        invent = float(inventstr.strip('g'))
    else:
        invent = 0
    print(invent)
    notes = member.find('NOTES')
    if notes is not None:
        notes = member.find('NOTES').text
    else:
        notes = ""
    print(notes)
    alternstr = member.find('SUBSTITUTES')
    if alternstr is not None:
        alternstr = member.find('SUBSTITUTES').text
    else:
        alternstr = ""
    print(alternstr)
    alphastr = member.find('ALPHA')
    if alphastr is not None:
        alphastr = member.find('ALPHA').text
        alpha = float(alphastr)
    else:
        alpha = 0
    print(alpha) 
    formstr = member.find('FORM')
    if formstr is not None:
        formstr = member.find('FORM').text
        if formstr == 'Pellet':
            form = 1
        else:
            form = 0
    else:
        form = 0
    print(form)
    sortstr = member.find('TYPE')
    if sortstr is not None:
        sortstr = member.find('TYPE').text
        if (sortstr == 'Aroma'):
            sort = 1
        elif (sortstr == 'Bittering'):
            sort = 2
        else:
            sort = 3
    else:
        sort = 1
    print(sort)
    origin = member.find('ORIGIN').text
    print(origin)

    cur.execute('''INSERT OR REPLACE INTO Hopfen (Name, Menge, Alpha, Pellets, Typ, Bemerkung, Eigenschaften, Alternativen) VALUES (?,?,?,?,?,?,?,?)''', (name, invent, alpha, form, sort, origin, notes, alternstr,))
    

cur.close()
conn.commit()
conn.close()





 
