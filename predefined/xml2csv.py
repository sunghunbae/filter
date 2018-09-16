#!/usr/bin/env python

import xml.etree.ElementTree as ET
import sys
import csv
import os

for filename in sys.argv[1:] :
    d = os.path.dirname(filename)
    b = os.path.basename(filename)
    p = b.split(".")[0]
    csvfilename = os.path.join(d,p+".csv")
    with open(filename,'rt') as f, open(csvfilename,"w") as csvfile:
        csvwriter = csv.writer(csvfile,delimiter=',',quotechar='"', 
                               quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["Name","SMARTS","Min","Max"])
        tree= ET.parse(f)
        for group in tree.findall("group"):
            name = group.get("name")
            smarts = group.find("SMARTS").text
            csvwriter.writerow([name,smarts,None,None])
        for descriptor in tree.findall("descriptor"):
            name = descriptor.get('name')
            L = descriptor.find('min')
            U = descriptor.find('max')
            lb = float(L.text) if L is not None else None
            ub = float(U.text) if U is not None else None
            csvwriter.writerow([name,None,lb,ub])
