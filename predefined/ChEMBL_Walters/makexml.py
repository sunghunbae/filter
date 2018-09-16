from __future__ import print_function
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from rdkit import Chem
import csv

sources= []

root= None
count= 0

with open("alert_collection.csv","r") as csvfile:
    rows = csv.reader(csvfile, delimiter=",",quotechar='"')
    next(rows) # skip header
    for row in rows:
        name, smarts, source= row[2],row[3],row[4]
        try:
            m= Chem.MolFromSmarts(smarts)
        except:
            print("INVALID SMARTS @", name, smarts, source)
            continue
        if not (source in sources):
            if len(sources) > 0:
                last_source = sources[-1]
                with open(last_source+".xml","w") as g:
                    coarse= tostring(root,'utf-8')
                    g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
            sources.append(source)
            root = Element(source)
            count = 0
        count += 1
        entry= SubElement (root, 'group')
        entry.set('name','('+str(count)+') '+name)
        sub= SubElement(entry,'SMARTS')
        sub.text = smarts

    last_source = sources[-1]
    with open(last_source+".xml","w") as g:
        coarse= tostring(root,'utf-8')
        g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
