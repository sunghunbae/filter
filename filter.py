# -*- coding: utf-8 -*-
from rdkit import Chem
from rdkit import RDLogger
from rdkit.Chem import Descriptors, rdMolDescriptors, Crippen
from rdkit.Chem.SaltRemover import SaltRemover
from multiprocessing import Pool
from operator import itemgetter
import multiprocessing as mp
import xml.etree.ElementTree as ET
import click
import csv
import sys
import os

log = RDLogger.logger()
log.setLevel(RDLogger.ERROR)

default_molId_prefix = 'X'

predefined_path = "./predefined"
predefined_filters={
    "Glaxo"       :"ChEMBL_Walters/Glaxo.xml",
#   "Glaxo"       :"Hann1999_Glaxo/Hann1999.xml",
    "Dundee"      :"ChEMBL_Walters/Dundee.xml",
#   "Brenk2008"   :"Brenk2008_Dundee/Brenk2008.xml",
    "BMS"         :"ChEMBL_Walters/BMS.xml",
    "Inpharmatica":"ChEMBL_Walters/Inpharmatica.xml",
    "SureChEMBL"  :"ChEMBL_Walters/SureChEMBL.xml",
    "LINT"        :"ChEMBL_Walters/LINT.xml",
    "MLSMR"       :"ChEMBL_Walters/MLSMR.xml",
    "PAINS"       :"Baell2010_PAINS/Baell2010A.xml",
    "PAINSa"      :"Baell2010_PAINS/Baell2010A.xml",
    "PAINSb"      :"Baell2010_PAINS/Baell2010B.xml",
    "PAINSc"      :"Baell2010_PAINS/Baell2010C.xml",
    "Toxicophore" :"Kazius2005/Kazius2005.xml",
    "Reactive"    :"misc/reactive.xml",
    "AstexRO3"    :"Astex-rule-of-3.xml",
    "Fragment"    :"Fragment.xml",
    "AsinexFrag"  :"Asinex-fragment.xml",
    "ZincFrag"    :"ZINC-fragment-like.xml",
    "Lead-Like"   :"ZINC-lead-like.xml",
    "Lipinski"    :"ZINC-Lipinski.xml",
    "Acid"        :"Hann1999_Glaxo/Hann1999Acid.xml",
    "Base"        :"Hann1999_Glaxo/Hann1999Base.xml",
    "Nucleophile" :"Hann1999_Glaxo/Hann1999NuPh.xml",
    "Electrophile":"Hann1999_Glaxo/Hann1999ElPh.xml",
    }

predefined_descriptors={
    "HAC"   : Descriptors.HeavyAtomCount,
    "HBA"   : Descriptors.NumHAcceptors,
    "LipinskiHBA": rdMolDescriptors.CalcNumLipinskiHBA,
    "HBD"   : Descriptors.NumHDonors,
    "LipinskiHBD": rdMolDescriptors.CalcNumLipinskiHBD,
    "rb"    : Descriptors.NumRotatableBonds,
    "ring"  : Descriptors.RingCount,
    "stereo": rdMolDescriptors.CalcNumAtomStereoCenters,
    "MolWt" : Descriptors.MolWt,
    "TPSA"  : Descriptors.TPSA,
    "logP"  : Descriptors.MolLogP,
    "FCsp3" : Descriptors.FractionCSP3,
    }

test_mols=[
    ("Sitagliptin",
    "Fc1cc(c(F)cc1F)C[C@@H](N)CC(=O)N3Cc2nnc(n2CC3)C(F)(F)F"), 
    ("Simvastatin",
     "O=C(O[C@@H]1[C@H]3C(=C/[C@H](C)C1)\C=C/[C@@H]([C@@H]3CC[C@H]2OC(=O)C[C@H](O)C2)C)C(C)(C)CC"),
    ("Sofosbuvir",
     "C[C@@H](C(OC(C)C)=O)N[P@](OC[C@@H]1[C@H]([C@@](F)([C@@H](O1)N2C=CC(NC2=O)=O)C)O)(OC3=CC=CC=C3)=O"),
    ]


def checkPredefined():
    """ check and show predefined filters and descriptors """
    print("  Checking Predefined Descriptors:")
    print("    %-15s   " % " ", 
        " ".join(["%12s" % name for name, smi in test_mols]))
    for k in predefined_descriptors:
        vals=[]
        for name, smi in test_mols:
            m= Chem.MolFromSmiles(smi)
            v= predefined_descriptors[k](m)
            if isinstance(v, int):
                vals.append("%12d" % v)
            else:
                vals.append("%12.3f" % v)
        print("    %-15s OK" % k," ".join(vals))
    print()
    print("  Checking Predefined Filters:")
    for k in predefined_filters:
        xml = predefined_filters[k]
        for name, smarts, lower, upper in parseXML(
            os.path.join(predefined_path,xml)):
            if smarts :
                m = Chem.MolFromSmarts(smarts)
                if m is None:
                    raise ValueError("%s %s %s" % (k,name,smarts))
            else:
                if not (name in predefined_descriptors):
                    raise ValueError("%s %s" % (k,name))
        print("    %-15s OK %s" % (k,predefined_filters[k]))

def showFilters(select_xmls={}, remove_xmls={}):
    """ show applied filters """
    print("  "+"-"*60)
    print("  Predefined Filters:")
    select_defs = select_xmls.copy()
    remove_defs = remove_xmls.copy()
    for k in predefined_filters:
        if k in remove_defs:
            print("  x %-15s %s" % (k, predefined_filters[k]))
            del remove_defs[k]
        elif k in select_defs:
            print("  o %-15s %s" % (k, predefined_filters[k]))
            del select_defs[k]
        else:
            print("    %-15s %s" % (k, predefined_filters[k]))
    if len(remove_defs) > 0 or len(select_defs) > 0:
        print("  Custom Filters:")
        for k in remove_defs:
            print("  x %-15s %s" % (k, remove_defs[k]))
        for k in select_defs:
            print("  o %-15s %s" % (k, select_defs[k]))
    print("  "+"-"*60)

def parseXML(filename):
    """ parse filter definitions in a XML format """
    data = []
    tree = ET.parse(filename)
    # parse substructure
    for group in tree.findall('group'):
        name = group.get('name')
        smarts = group.find('SMARTS').text
        data.append((name,smarts,None,None))
    # parse descriptors
    for descriptor in tree.findall('descriptor'):
        name = descriptor.get('name')
        L = descriptor.find('min')
        U = descriptor.find('max')
        lb = float(L.text) if L is not None else None
        ub = float(U.text) if U is not None else None
        data.append((name,None,lb,ub))
    return data

def readFilters(select_xmls, remove_xmls):
    """ read filter definitions """
    fs = []
    for name in select_xmls:
        fs.append((name,'select',
            parseXML(os.path.join(predefined_path,select_xmls[name]))))
    for name in remove_xmls:
        fs.append((name,'remove',
            parseXML(os.path.join(predefined_path,remove_xmls[name]))))
    return fs 


def getMatchedFilter(s):
    """ get the best matching filter name """
    t = s.upper()
    n = len(t)
    for k in predefined_filters:
        if k.upper()[:n] == t:
            return (k, predefined_filters[k])
    return None,None
        
def getxmls(filters):
    xmls={}
    for k in filters:
        if os.path.exists(k):
            name = os.path.basename(k).split(".")[0]
            xmls[name]= k
        else:
            name,path = getMatchedFilter(k)
            if path :
                xmls[name] = path
            else:
                print("Error: '%s' not found nor matching with predefined" % k)
                showFilters()
                sys.exit(1)
    return xmls


def worker( load ):
    m,molId,action,filtername,entryname,smarts,lb,ub = load
    flag = False # does it have the substr or descriptor within the range
    if smarts: # substructure matching
        query= Chem.MolFromSmarts(smarts)
        found = m.GetSubstructMatches(query)
        v = len(found)
        vstr = str(v)
        if v > 0 : flag = True
    else: # descriptor range matching
        v = predefined_descriptors[entryname](m)
        if isinstance(v,int):
            vstr = str(v)
        else:
            vstr = '%10.3f' % v
        # return if lower and upper boundaries are satisfied
        if ((not lb) or (v >= lb)) and ((not ub) or (v <= ub)): flag = True
    return (flag,action,molId,filtername,entryname,vstr,lb,ub)

def guessIdentity(mols):
    f={}
    for m in mols:
        if m is None: continue
        props = m.GetPropsAsDict()
        for k in props:
            v = props[k]
            # float is not suitable for molId
            if isinstance(v,float): continue 
            if not (k in f): f[k]=set()
            if isinstance(v,int): 
                f[k].add(str(v))
            else:
                f[k].add(v)
    r=[]
    for k in f:
        r.append((k,len(f[k]), -max([len(x) for x in f[k]]))) 
    r=sorted(r, key=itemgetter(1,2))
    identity= r[-1][0]
    print("suggested identity is '"+identity+"'")
    return identity
    

@click.command()
@click.option('--verbose/--quiet',default=False)
@click.option('--remove', '-r', multiple=True)
@click.option('--select', '-s', multiple=True)
@click.option('--identity', help="SDF property name for molecule ID")
@click.option('--check',is_flag=True,is_eager=True,help="Check predefined filters")
@click.option('--cpu', default=mp.cpu_count(),help="Number of CPUs to use")
@click.argument('filename')
def main(filename,remove,select,identity,verbose,check,cpu):

    """ remove or select molecules by using predefined or custom filters """

    if check: 
        checkPredefined()
        sys.exit(0)

    select_xml= getxmls(select)
    remove_xml= getxmls(remove)
    showFilters(select_xml,remove_xml)
    FS = readFilters(select_xml,remove_xml)

    b= os.path.basename(filename)
    prefix= b.split(".")[0]
    ext= b.split(".")[-1].lower()

    if ext == "smi" or ext == "smiles" or ext == "ism" :
        mols = Chem.SmilesMolSupplier(filename,titleLine=False)
        outfile = prefix+"-selected.smi"
        outWriter = Chem.SmilesWriter(outfile,includeHeader=False,delimiter=' ')
    elif ext == "sdf" or ext == "sd" :
        mols = Chem.SDMolSupplier(filename)
        outfile = prefix+"-selected.sdf"
        outWriter = Chem.SDWriter(outfile)

    logfile = prefix+"-rejected.csv"
    f = open(logfile,"w")
    logWriter= csv.writer(f,delimiter=",",quotechar='"')

    p = Pool(cpu)

    # test molId with the first record
    if identity:
        try:
            Id =  mols[0].GetProp(identity)
            assert Id
        except:
            print("Error: cannot define Id by given 'identity'")
            sys.exit(9)
    else:
        if mols[0].GetProp("_Name"): 
            identity= "_Name"
        else:
            identity= guessIdentity(mols)

    num = 0
    num_records= 0
    num_remove = 0
    num_select = 0
    done= []
    for m in mols :
        num_records += 1
        if m == None : continue
        Id = m.GetProp(identity)
        if (not Id) or (Id in done):
            Id = default_molId_prefix+"%04d" % num
        m.SetProp("_Name",Id)
        m = SaltRemover().StripMol(m, dontRemoveEverything=True)
        workload = []
        for filtername,action,entries in FS :
            workload.extend([(m,Id,action,filtername,grp,smarts,lb,ub) \
                for grp,smarts,lb,ub in entries])

        results = list(p.map(worker, workload))

        vote_to_remove = 0
        vote_to_select = 0
        reasons= []
        for res in results:
            flag,action,molId,vstr,filtername,entryname,lb,ub = res
            if (flag == True  and action == "select") or \
               (flag == False and action == "remove") :
                vote_to_select += 1
            else:
                vote_to_remove += 1
                reasons.append(res)

        # verdict
        if vote_to_remove > 0:
            num_remove += 1
            for res in reasons:
              logWriter.writerow(res) # rejected
              if verbose: print("  %-10s %s %-30s %10s [%s..%s]" % res[2:])
        else:
            num_select += 1
            outWriter.write(m) # passed
        
        done.append(Id)
        num += 1

    num_done = len(done)
    print("%d/%d done     <-- %s" % (num_done,num_records,filename))
    print("%d/%d selected --> %s" % (num_select,num_done,outfile))
    print("%d/%d rejected --> %s" % (num_remove,num_done,logfile))

if __name__ == "__main__" :
    main()
