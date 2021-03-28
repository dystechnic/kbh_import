import xml.etree.ElementTree as ET
import sqlite3
import sys

conn = sqlite3.connect('kb_daten.sqlite')
print('Connected to database successfully.')
cur = conn.cursor()
print("\n [+] Cursor has been set up successfully")

#filename = "miscs.xml"
filename = sys.argv[-1]
tree = ET.parse(filename)
root = tree.getroot()

"""
Fields in weiterezutaten table  <==>   Fields in BeerXML Fermentables
Name                            <==>   NAME
Menge                           <==>   INVENTORY
Einheit                         <==>   g = 1   kg = 0
Typ                             <==>   TYPE 
                                       0 = Honing
                                       1 = Suiker
                                       2 = Specerij => Spice
                                       3 = Fruit 
                                       4 = Diversen => Other, Flavor
                                       5 = Kruiden => Herb
                                       6 = Waterbehandeling => Water agent
                                       7 = Klaringsmiddel => Fining
Ausbeute                        
Farbe                           
MAX_IN_BATCH                    <==>
Bemerkung                       <==>   USE_FOR
Eigenschaften                   <==>   NOTES
Alternativen
Preis
Eingelagert
Mindesthaltbar
Link
"""
for member in root.findall('MISC'):
    name = member.find('NAME')
    if name is not None:
        name = member.find('NAME').text
        print(name)
    notes = member.find('NOTES')
    if notes is not None:
        notes = member.find('NOTES').text
    else:
        notes = ""
    use = member.find('USE_FOR')
    if use is not None:
        use = member.find('USE_FOR').text
    else:
        use = ""
    print(use)
    inventstr = member.find('INVENTORY')
    if inventstr is not None:
        inventstr = member.find('INVENTORY').text
        invent = float(inventstr.strip('g)'))
    else:
        invent = 0
    print(invent)
    typstr = member.find('TYPE')
    if typstr is not None:
        typstr = member.find('TYPE').text
        if (typstr == "Spice"):
            typ = 2
        if (typstr == 'Other'):
            typ = 4
        if (typstr == 'Flavor'):
            typ = 4
        if (typstr == 'Herb'):
            typ = 5
        if (typstr == 'Water agent'):
            typ = 6
        if (typstr == 'Fining'):
            typ = 7
    else:
        typ = 4
        
    print(typstr)
    print(typ)            
    
    cur.execute('''INSERT OR REPLACE INTO WeitereZutaten (Name, Menge, Einheit, Typ, Bemerkung, Eigenschaften) VALUES (?,?,?,?,?,?)''', (name, invent, 1, typ, use, notes,))
# Eenheid in xml is standaard gram,dus 1.    



cur.close()
conn.commit()
conn.close()
