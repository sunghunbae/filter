from xml.etree.ElementTree import Element,SubElement,Comment,tostring,parse
from xml.dom import minidom

A= Element('PAINS')
A.append(Comment('Filter Family A p.S23'))

B= Element('PAINSb')
B.append(Comment('Filter Family B S23-S25'))

C= Element('PAINSc')
C.append(Comment('Filter Family C S25-S37'))

with open('PAINS-more-than-150-hits.xml','rt') as f :
	treeA= parse(f)
with open('PAINS-less-than-150-hits.xml','rt') as g :
	treeB= parse(g)
with open('PAINS-less-than-015-hits.xml','rt') as h :
	treeC= parse(h)

count= 0
for node in treeA.iter() :
	if node.tag == 'SMART' :
		smarts= node.text.strip()
	if node.tag == 'name' :
		name= node.text.strip()
		count += 1
		entry= SubElement (A, 'group')
		entry.set('name', '('+str(count)+') '+name)
		node= SubElement (entry, "SMARTS")
		node.text= smarts

count= 0
for node in treeB.iter() :
	if node.tag == 'SMART' :
		smarts= node.text.strip()
	if node.tag == 'name' :
		name= node.text.strip()
		count += 1
		entry= SubElement (B, 'group')
		entry.set('name', '('+str(count)+') '+name)
		node= SubElement (entry, "SMARTS")
		node.text= smarts

count= 0
for node in treeC.iter() :
	if node.tag == 'SMART' :
		smarts= node.text.strip()
	if node.tag == 'name' :
		name= node.text.strip()
		count += 1
		entry= SubElement (C, 'group')
		entry.set('name', '('+str(count)+') '+name)
		node= SubElement (entry, "SMARTS")
		node.text= smarts
	

g=open('Baell2010A.xml','wt')
coarse= tostring(A,'utf-8')
g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
g.close()

g=open('Baell2010B.xml','wt')
coarse= tostring(B,'utf-8')
g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
g.close()

g=open('Baell2010C.xml','wt')
coarse= tostring(C,'utf-8')
g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
g.close()
