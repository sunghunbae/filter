from xml.etree.ElementTree import Element,SubElement,Comment,tostring,parse
from xml.dom import minidom

count= 0
A= Element('reactive')

for (name, smarts) in [
  ["4-Nitrophenyl Ester","[O-][N+](=O)c1ccc(OC=O)cc1"],
  ["Acid Chloride","C(=O)Cl"],
  ["Acid Bromide","C(=O)Br"],
  ["Acid Iodide","C(=O)I"],
  ["Acid Fluoride","C(=O)F"],
  ["Acyl Cyanide","N#CC(=O)"],
  ["Acyl hydrazine","NNC=O"],
  ["Anhydride","C(=O)OC(=O)"],
  ["Allyl Bromide","BrCC=C"],
  ["Allyl Chloride","ClCC=C"],
  ["Allyl Fluoride","FCC=C"],
  ["Allyl iodide","ICC=C"],
  ["Alpha_HaloCarbonyl","[F,Cl,Br,I]CC=O"],
  ["Beta_HaloCarbonyl","[F,Cl,Br,I]CCC=O"],
  ["Azide","N=[N+]=[N-]"],
  ["Aziridine","C1CN1"],
  ["Azo","[N;X2]=[N;X2]"],
  ["Benzyl Bromide","[H]C([H])(Br)c"],
  ["Benzyl Chloride","[H]C([H])(Cl)c"],
  ["Benzyl Iodide","[H]C([H])(I)c"],
  ["Beta ammonium carbonyl","C[N+](C)(C)CCC=O"],
  ["Carbazide","O=*N=[N+]=[N-]"],
  ["Carbodimide","N=C=N"],
  ["Chloramine","[N;X3](Cl)"],
  ["Chloro Silane","Cl[Si]"],
  ["Cyanohydrin","N#CC[OH]"],
  ["cyanamides","N[CH2]C#N"],
  ["Cyanate","O=C=N"],
  ["diazo","cN=Nc"],
  ["Diazonium","[N+]#N"],
  ["Dichloramine","[N;X3](Cl)Cl"],
  ["Disulphide","SS"],
  ["Epoxide","C1CO1"],
  ["HaloAmine","[F,Cl,Br,I]N"],
  ["Beta_HaloAmine","[F,Cl,Br,I]CCN"],
  ["HaloMethylEther","[F,Cl,Br,I]C[OH0;X2]"],
  ["HaloMethylThioEther","[F,Cl,Br,I]C[SH0;X2]"],
  ["HydroxyBenzoylTriazole","C(=O)Onnn"],
  ["Imidoyl Chloride","ClC=N"],
  ["Imidoyl Bromide","BrC=N"],
  ["Iodoso","I(=O)"],
  ["Iodoxy","O=I=O"],
  ["Isocyanate","N=C=O"],
  ["Isothiocyanate","N=C=S"],
  ["isonitriles","[N+]#[C-]"],
  ["Ketene","C=C=O"],
  ["Lawesson's_reagents","P(=S)(S)S"],
  ["Nitroso","[N;X2]=O"],
  ["Oxaziridine","C1NO1"],
  ["Pentafluorophenyl Ester","Fc1c(F)c(F)c(OC=O)c(F)c1F"],
  ["Peroxide","OO"],
  ["Phosphine Chloride","PCl"],
  ["Phosphine Bromide","PBr"],
  ["Phosphine Fluoride","PF"],
  ["Phosphine Iodide","PI"],
  ["Cationic Br","[Br+]"],
  ["Cationic Cl","[Cl+]"],
  ["Cationic I","[I+]"],
  ["Cationic O","[O+,o+]"],
  ["Cationic P","[P+]"],
  ["Cationic S","[S+]"],
  ["Sulphonyl Chloride","S(=O)(=O)[Cl]"],
  ["Sulphonyl Bromide","S(=O)(=O)[Br]"],
  ["Sulphonyl Fluoride","S(=O)(=O)[F]"],
  ["Sulphonate Ester","COS(c)(=O)=O"],
  ["Sulphonyl Cyanide","S(=O)(=O)C#N"],
  ["Thioacyl Chloride","C(=S)Cl"],
  ["Thioacyl  Bromide","C(=S)Br"],
  ["Thio Halides","[S][Cl,Br,F,I]"],
  ["Thiocyanate","SC#N"],
  ["Triflate","OS(=O)(=O)C(F)(F)F"],
  ["Vinylous Acid Chloride","ClC=CC=O"]
  ]:
     count += 1
     entry= SubElement (A, 'group')
     entry.set('name', '('+str(count)+') '+name)
     node= SubElement(entry, "SMARTS")
     node.text= smarts
   
with open('reactive-part1.xml','rt') as f :
	treeA= parse(f)

with open('reactive-part2.xml','rt') as g :
	treeB= parse(g)


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

for node in treeB.iter() :
	if node.tag == 'SMART' :
		smarts= node.text.strip()
	if node.tag == 'name' :
		name= node.text.strip()
		count += 1
		entry= SubElement (A, 'group')
		entry.set('name', '('+str(count)+') '+name)
		node= SubElement (entry, "SMARTS")
		node.text= smarts

g=open('reactive.xml','wt')
coarse= tostring(A,'utf-8')
g.write( minidom.parseString( coarse ).toprettyxml(indent="  ") )
g.close()
