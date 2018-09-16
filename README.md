# filter

Remove or select molecules with predefined substructures and descriptors

## Requirement

* Python 3.6
* RDKit

## Usage

```
Usage: filter.py [OPTIONS] FILENAME

  remove or select molecules by using predefined or custom filters

Options:
  --verbose / --quiet
  -r, --remove TEXT
  -s, --select TEXT
  --identity TEXT      SDF property name for molecule ID
  --check              Check predefined filters
  --cpu INTEGER        Number of CPUs to use
  --help               Show this message and exit.
```

```$ python filter.py --check a```

Show all predefined filters and descriptors. 
Please note that an arbitrary filename "a" is given here.

```$ python filter.py test/test.sdf --identity ID --remove lint```

Remove compounds that match LINT filters. `--identity` option is used to find a
unique molecular name in case where the first line of SDF file is blank.
If `--identity` option is omitted, it tries to guess a most suitable identity using
the properties.
Predefined or custom filters can be used after `--remove` or `--select` options.
A cloest matching and case insensitive fiter names are accepted.

```$ python filter.py test/test.sdf -r inphar -s zincfrag```

Remove compounds that match Inpharmatica filter and select ZINC fragment definition.
`--remove (or -r)` and `--select (or -s)` can be used at the same time.


## Predefined filters

Name | Description | Reference 
---- | ----------- | ---------
PAINS | Pan Assay Interference Compounds (PAINS) (>150 hits)    | Baell et al. (2010)
PAINSa | Pan Assay Interference Compounds (PAINS) (>150 hits)    | Baell et al. (2010)
PAINSb | Pan Assay Interference Compounds (PAINS) (15-150 hits) | Baell et al. (2010) 
PAINSc | Pan Assay Interference Compounds (PAINS) (<15 hits)    | Baell et al. (2010)
Dundee | NTD Screening Library | Brenk et al. (2008)
BMS    | HTS Deck Filters      | Pearce et al. (2006)
Glaxo  | Hard Filters          | Hann et al. (1999)
LINT   | Pfizer LINT Filters | Blake (2005)
MLSMR  | NIH Molecular Libraries Small Molecule Repository <br>Excluded Functionality Filters | Dandapani et al. (2012)
Inpharmatica | Unwanted Fragments | ChEMBL
Toxicophore  | Toxicophores for Mutagenicity Prediction | Kazius et al. (2005)
ALARM | Abott ALARM NMR Filters for Reactive Compounds | Huth et al. (2005)
SureChEMBL | SureChEMBL filter | ChEMBL
Reactive | reactive functional group | 
AstexRO3 | Astex rule of 3 | Astex
Fragment | fragment |
AsinexFrag |  Asinex's fragment | Asinex
ZincFrag  | ZINC's fragment-like | ZINC
Lead-Like | ZINC's lead-like | ZINC
Lipinski  | ZINC's drug-like | ZINC
Acid | acid | Hann et al. (1999)
Base | base | Hann et al. (1999)
Nucleophile | nucleophile | Hann et al. (1999)
Electrophile | electrophile | Hann et al. (1999)


## Predefined descriptors

All descriptor calculations use RDKit

Name | Description
---- | -----------
HAC | Heavyatom (non-hydrogen atom) count  
HBA | Number of hydrogen bond acceptor
LipinskiHBA | Number of Lipinski's Hydrogen bond acceptor
HBD | Number of hydrogen bond donor
LipinskiHBD | Number of Lipinski's Hydrogen bond donor
rb | Number of rotatable bond
ring | Number of rings
stereo | Number of atom stereo centers
MolWt | Molecular weight
TPSA | Topological polar surface area
logP | log(partition coefficient between octanol and water)
FCsp3 | Fraction of Sp3 carbons

## Examples of filters

All filters are defined in XML format and easy to read, write and modify. 

`predefined/ChEMBL_Walters/Glaxo.xml`

```xml
<?xml version="1.0" ?>
<Glaxo>
  <group name="(1) R1 Reactive alkyl halides">
    <SMARTS>[Br,Cl,I][CX4;CH,CH2]</SMARTS>
  </group>
  <group name="(2) R2 Acid halides">
    <SMARTS>[S,C](=[O,S])[F,Br,Cl,I]</SMARTS>
  </group>
  ...
</Glaxo>
```

`predefined/ZINC-Lipinski.xml`

```xml
<?xml version="1.0" ?>
<ZINC-Lipinski>
  <!--definition from zinc.docking.org -->
  <!--Lipinski, J Pharmacol Toxicol Methods. 2000 Jul-Aug;44(1):235-49.-->
  <descriptor name="MolWt">
    <min>150</min>
    <max>500</max>
  </descriptor>
  <descriptor name="logP">
    <max>5.0</max>
  </descriptor>
 ...
</ZINC-Lipinski>
```


## References

1. `alert_collection.csv` is copied from Patrick Walters' blog and github:
    - http://practicalcheminformatics.blogspot.com/2018/08/filtering-chemical-libraries.html
    - https://github.com/PatWalters/rd_filters


1. Huth JR, Mendoza R, Olejniczak ET, Johnson RW, Cothron DA, Liu Y, Lerner CG, Chen J, Hajduk PJ. ALARM NMR: a rapid and robust experimental method to detect reactive false positives in biochemical screens. J Am Chem Soc. 2005, 127, 217-24.

1. Jeroen Kazius, Ross McGuire, and Roberta Bursi. Derivation and Validation of Toxicophores for Mutagenicity Prediction. J. Med. Chem. 2005, 48, 312-320.

1. J. F. Blake. Identification and Evaluation of Molecular Properties Related to Preclinical Optimization and Clinical Fate. Med Chem. 2005, 1, 649-55.

1. Mike Hann, Brian Hudson, Xiao Lewell, Rob Lifely, Luke Miller, and Nigel Ramsden. Strategic Pooling of Compounds for High-Throughput Screening. J. Chem. Inf. Comput. Sci. 1999, 39, 897-902.

1. Jonathan B. Baell and Georgina A. Holloway. New Substructure Filters for Removal of Pan Assay Interference Compounds (PAINS) from Screening Libraries and for Their Exclusion in Bioassays. J. Med. Chem. 2010, 53, 2719-2740.

1. Bradley C. Pearce, Michael J. Sofia, Andrew C. Good, Dieter M. Drexler, and David A. Stock. An Empirical Process for the Design of High-Throughput Screening Deck Filters. J. Chem. Inf. Model. 2006, 46, 1060-1068.

1. Ruth Brenk, Alessandro Schipani, Daniel James, Agata Krasowski, Ian Hugh Gilbert, Julie Frearson aand Paul Graham Wyatt. Lessons learnt from assembling screening libraries for drug discovery for neglected diseases. ChemMedChem. 2008, 3, 435-44.

1. Sivaraman Dandapani, Gerard Rosse, Noel Southall, Joseph M. Salvino, Craig J. Thomas. Selecting, Acquiring, and Using Small Molecule Libraries for High‐Throughput Screening. Curr Protoc Chem Biol. 2012, 4, 177–191.
