from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

root= Element('Brenk2008')
root.append(Comment('Table S1. Definition of unwanted groups'))

f=open('Brenk_et_al-2008-ChemMedChem-SI.txt','rt')
count= 0
for line in f :
	c=line.strip().split('\t')
	count += 1
	entry= SubElement (root, 'group')
	entry.set('name', '('+str(count)+') '+c[0].strip())
	node= SubElement (entry, 'SMARTS')
	node.text= c[1].strip()
f.close()


g=open('Brenk2008.xml','wt')
coarse= tostring(root,'utf-8')
g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
