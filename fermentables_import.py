import xml.etree.ElementTree as ET
import sqlite3
import sys

conn = sqlite3.connect('kb_daten.sqlite')
print('Connected to database successfully.')
cur = conn.cursor()
print("\n [+] Cursor has been set up successfully")

filename = "fermentables.xml"
#filename = sys.argv[-1]
tree = ET.parse(filename)
root = tree.getroot()

"""
Fields in malz table  <==>   Fields in BeerXML Fermentables
Name                  <==>   NAME
Menge                 <==>   INVENTORY
Potential             
Farbe                 <==>   DISPLAY_COLOR
pH                    <==>   DI_pH
MaxProzent            <==>   MAX_IN_BATCH
Bemerkung             
Eigenschaften         <==>   NOTES
Preis
Eingelagert
Mindesthaltbar
Link
"""
for member in root.findall('FERMENTABLE'):
    name = member.find('NAME')
    if name is not None:
        name = member.find('NAME').text
        print(name)
    inventstr = member.find('INVENTORY')
    if inventstr is not None:
        inventstr = member.find('INVENTORY').text
        invent = float(inventstr.strip('kg)'))
    else:
        invent = 0
    print(invent)
    colorstr = member.find('DISPLAY_COLOR')
    if colorstr is not None:
        colorstr = member.find('DISPLAY_COLOR').text
        color = float(colorstr.strip('EBC')) 
    else:
        color= 0
    print(color) 
    phstr = member.find('DI_pH')
    if phstr is not None:
        phstr = member.find('DI_pH').text
        ph = float(phstr)
    else:
        ph = 0
    print(ph)
    batchmaxstr = member.find('MAX_IN_BATCH')
    if batchmaxstr is not None:
        batchmaxstr = member.find('MAX_IN_BATCH').text
        batchmax = float(batchmaxstr)
    else:
        batchmax = 100
    print(batchmax)
    notes = member.find('NOTES')
    if notes is not None:
        notes = member.find('NOTES').text
    else:
        notes = ""
    print(notes)
    
    
    cur.execute('''INSERT OR REPLACE INTO Malz (Name, Menge, Farbe, pH, Maxprozent, Eigenschaften) VALUES (?,?,?,?,?,?)''', (name, invent, color, ph, batchmax, notes,))
    

cur.close()
conn.commit()
conn.close()





 
