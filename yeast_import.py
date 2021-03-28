import xml.etree.ElementTree as ET
import sqlite3
import sys

conn = sqlite3.connect('kb_daten.sqlite')
print('Connected to database successfully.')
cur = conn.cursor()
print("\n [+] Cursor has been set up successfully")

#filename = "yeasts.xml"
filename = sys.argv[-1]
tree = ET.parse(filename)
root = tree.getroot()

"""
Fields in hefen table <==>   Fields in BeerXML Hops
Name                   <==>   NAME (text)
Menge
TypOGUG                <==>   type gist (can't find it in XML)
TypTrFl                <==>   FORM (Dry = 1, Liquid = 2) (integer)
Wuerzemenge             
Sedimentation          <==>   FLOCCULATION (text)
EVG                    <==>   ATTENUATION (text)
Temperatur             <==>   DISP_MIN_TEMP + DISP_MAX_TEMP (text)
Bemerkung              <==>   ORIGIN (text)
Eigenschaften          <==>   NOTES (text)
Alternativen
Preis
Eingelagert              
Mindesthaltbar
Link
"""
for member in root.findall('YEAST'):
    name = member.find('NAME')
    if name is not None:
        name = member.find('NAME').text
    print(name)
    notes = member.find('NOTES')
    if notes is not None:
        notes = member.find('NOTES').text
        print(notes)
    else:
        notes = ""
    mintempstr = member.find('DISP_MIN_TEMP')
    if mintempstr is not None:
        mintempstr = member.find('DISP_MIN_TEMP').text
    else:
        mintempstr = "0 °C"
    maxtempstr = member.find('DISP_MAX_TEMP')
    if maxtempstr is not None:
        maxtempstr = member.find('DISP_MAX_TEMP').text
    else:
        maxtempstr = "0 °C"       
    temp = mintempstr +" - "+ maxtempstr
    print(temp)
    formstr = member.find('FORM')
    if formstr is not None:
        formstr = member.find('FORM').text
        if formstr == 'Dry':
            form = 1
        else:
            form = 2
    else:
        form = 1
    print(form)
    floccstr = member.find('FLOCCULATION')
    if floccstr is not None:
        floccstr = member.find('FLOCCULATION').text
    else:
        floccstr = ""
    print(floccstr)
    attstr = member.find('ATTENUATION')
    if attstr is not None:
        attstr = member.find('ATTENUATION').text
    else:
        attstr = ""
    print(attstr)
    originstr = member.find('ORIGIN')
    if originstr is not None:
        originstr = member.find('ORIGIN').text
        print(originstr)
    else:
        originstr = ""
    print(originstr)

    cur.execute('''INSERT OR REPLACE INTO Hefe (Name, TypTrFl, Sedimentation, EVG, Temperatur, Bemerkung, Eigenschaften) VALUES (?,?,?,?,?,?,?)''', (name, form, floccstr, attstr, temp, originstr, notes,))
    

cur.close()
conn.commit()
conn.close()





 
