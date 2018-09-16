from __future__ import print_function
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from rdkit import Chem
import sys

with open("hann1999filter.txt","r") as f, \
     open("Hann1999.xml","w") as g:
  root= Element('Hann1999')
  for line in f :
    if line.startswith("#") : continue 
    c= line.strip().split()
    if len(c) < 2 : continue
    try:
      smartstxt= c[-1]
      name= " ".join(c[:-1])
    except:
      print(line.rstrip())
      sys.exit(0)
    try:
      rdkq= Chem.MolFromSmarts(smartstxt)
    except:
      print("NOT VALID:", line.rstrip())
      continue
    entry= SubElement (root, 'group')
    entry.set('name', name)
    node= SubElement (entry, 'SMARTS')
    node.text= smartstxt
  # write to XML
  coarse= tostring(root,'utf-8')
  g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )

with open("hann1999acid.txt","r") as f, \
     open("Hann1999Acid.xml","w") as g:
  root= Element('Hann1999')
  for line in f :
    if line.startswith("#") : continue 
    c= line.strip().split()
    if len(c) < 2 : continue
    try:
      smartstxt= c[-1]
      name= " ".join(c[:-1])
    except:
      print(line.rstrip())
      sys.exit(0)
    try:
      rdkq= Chem.MolFromSmarts(smartstxt)
    except:
      print("NOT VALID:", line.rstrip())
      continue
    entry= SubElement (root, 'group')
    entry.set('name', name)
    node= SubElement (entry, 'SMARTS')
    node.text= smartstxt
  # write to XML
  coarse= tostring(root,'utf-8')
  g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )

with open("hann1999acid.txt","r") as f, \
     open("Hann1999Acid.xml","w") as g:
  root= Element('Hann1999')
  for line in f :
    if line.startswith("#") : continue 
    c= line.strip().split()
    if len(c) < 2 : continue
    try:
      smartstxt= c[-1]
      name= " ".join(c[:-1])
    except:
      print(line.rstrip())
      sys.exit(0)
    try:
      rdkq= Chem.MolFromSmarts(smartstxt)
    except:
      print("NOT VALID:", line.rstrip())
      continue
    entry= SubElement (root, 'group')
    entry.set('name', name)
    node= SubElement (entry, 'SMARTS')
    node.text= smartstxt
  # write to XML
  coarse= tostring(root,'utf-8')
  g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
