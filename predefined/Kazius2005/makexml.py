from xml.etree.ElementTree import Element,SubElement,Comment,tostring,parse
from xml.dom import minidom
from rdkit import Chem

""" 
Jeroen Kazius, Ross McGuire, and Roberta Bursi, 2004. 
Derivation and Validation of Toxicophores for Mutagenicity Prediction. 
J. Med. Chem., 2005, 48 (1), pp 312–320 DOI: 10.1021/jm040835a
"""

count= 0
A= Element('Kazius2005')

for (name, smarts) in [
  ["Aromatic nitro","a[$([NX3](=O)=O),$([NX3+](=O)[O-])][!#8]"],
  ["Aromatic amine","a[NX3;H2]"],
  ["3-membered heterocycle","[N,O,S]1[C][C]1"],
  ["unsubstituted heteroatom bonded heteroatom","[NX2;H2,OX1;H1][N,O]"],
  ["Specific aromatic nitro","$(O=N(~O)a);!$(O=N(O)c[$(aS(=O)=O),$(aaS(=O)=O),$(aaaS(=O)=O),$(aC((F)F)F),$(aaC((F)F)F),$(aaaC((F)F)F)])"],
  ["Specific aromatic amine","a[NH2]"],
  ["aromatic nitroso","a[N;X2]=O"],
  ["alkyl nitrite","CO[N;X2]=O"],
  ["nitrosamine","N[N;X2]=O"],
  ["epoxide","O1[c,C]-[c,C]1"],
  ["aziridine","C1NC1"],
  ["azide","N=[N+]=[N-]"],
  ["diazo","C=[N+]=[N-]"],
  ["triazene","N=N-N"],
  ["unsubstituted heteroatom-bonded heteroatom","[OH,NH2][N,O]"],
  ["aromatic hydroxylamine","[OH]Na"],
  ["aliphatic halide","[Cl,Br,I]C"],
  ["carboxylic acid halide","[Cl,Br,I]C=O"],
  ["nitrogen or sulphur mustard","[N,S]!@[C;X4]!@[CH2][Cl,Br,I]"],
  ["bay-region in Polycyclic Aromatic Hydrocarbons","[cH]1[cH]ccc2c1c3c(cc2)cc[cH][cH]3"],
  ["K-region in Polycyclic Aromatic Hydrocarbons","[cH]1cccc2c1[cH][cH]c3c2ccc[cH]3"],
  ["sulphonate-bonded carbon (alkyl alkane sulphonate or dialkyl sulphate)","[$([C,c]OS(=O)(=O)O!@[c,C]),$([c,C]S(=O)(=O)O!@[c,C])]"],
  ["aliphatic N-nitro","O=N(~O)N"],
  ["aB unsaturated aldehyde (including a-carbonyl aldehyde)","[$(O=[CH]C=C),$(O=[CH]C=O)]"],
  ["diazonium","[N;v4]#N"],
  ["beta-propiolactone","O=C1CCO1"],
  ["ab unsaturated alkoxy group","[CH]=[CH]O"],
  ["1-aryl-2-monoalkyl hydrazine","[NH;!R][NH;R]a"],
  ["aromatic methylamine","[CH3][NH]a;![CH3][NH]a[$(a[$(C((F)F)F),$(S=O),$(C(=O)O)]),$(aa[$(C((F)F)F),$(S=O),$(C(=O)O)]),$(aaa[$(C((F)F)F),$(S=O),$(C(=O)O)])]"],
  ["ester derivative of aromatic hydroxylamine (including original specific toxicophore)","aN([$([OH]),$(O*=O)])[$([#1]),$(C(=O)[CH3]),$([CH3]),$([OH]),$(O*=O)]"],
  ["polycyclic planar system 1","a13~a~a~a~a2~a1~a(~a~a~a~3)~a~a~a~2"],
  ["polycyclic planar system 2","a1~a~a~a2~a~1~a~a3~a(~a~2)~a~a~a~3"],
  ["polycyclic planar system 3","a1~a~a~a2~a~1~a~a~a3~a~2~a~a~a~3"],
  ["polycyclic planar system 4","a1~a~a~a~a2~a~1~a3~a(~a~2)~a~a~a~a~3"],
  ["polycyclic planar system 5","a1~a~a~a~a2~a~1~a~a3~a(~a~2)~a~a~a~3"],
  ["polycyclic planar system 6","a1~a~a~a~a2~a~1~a~a3~a(~a~2)~a~a~a~a~3"],
  ["polycyclic planar system 7","a1~a~a~a~a2~a~1~a~a~a3~a~2~a~a~a~3"],
  ["polycyclic planar system 8","a1~a~a~a~a2~a~1~a~a~a3~a~2~a~a~a~a~3"],
  ["polycyclic planar system 9","a13~a~a~a~a2~a1~a(~a~a~a~3)~a~a~2"],
     ]:
     m = Chem.MolFromSmarts(smarts)
     if m is None: continue
     count += 1
     entry= SubElement (A, 'group')
     entry.set('name', '('+str(count)+') '+name)
     node= SubElement(entry, "SMARTS")
     node.text= smarts
   
g=open('Kazius2005.xml','wt')
coarse= tostring(A,'utf-8')
g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
g.close()
