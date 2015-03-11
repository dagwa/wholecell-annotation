# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 16:53:05 2015

@author: tral
"""

IDORG="http://identifiers.org/"

CV_SOURCES = {
	"ATCC": IDORG+"atcc/",
	"BiGG": "http://bigg.ucsd.edu/bigg/postMet.pl?organism=3307911&organism=1461534&organism=222668&organism=3277493&organism=2795088&organism=2423527&organism=1823466&compartment_list=any&pathway_list=any&name_text=",
      #no entry in identifiers.org 
	"BioCyc": "http://biocyc.org/MGEN243273/NEW-IMAGE?type=GENE&object=", #type=GENE does not work via identifiers.org
	"BioProject": IDORG+"bioproject/",
	"CAS": IDORG+"cas/", #Karr (2011) uses other URL 
	"ChEBI": IDORG+"ChEBI/CHEBI:",
	"CMR": IDORG+"cmr.gene/",#resource offline, deprecated!
	"EC": IDORG+"ec-code/",
	"GenBank": IDORG+"insdc/",#Karr (2011) uses wrong URL
	"ISBN": "http://isbndb.com/search-all.html?kw=%s",
	"KEGG": IDORG+"kegg.compound/",
	"KNApSAcK": IDORG+"knapsack/",
	"LipidBank": IDORG+"lipidbank/",
	"LIPIDMAPS": IDORG+"lipidmaps/",
	"PDB": IDORG+"pdb/",
	"PDBCCD": IDORG+"pdb.ligand/",
	"PubChem": IDORG+"pubchem.substance/",
	"PubMed": "http://www.ncbi.nlm.nih.gov/pubmed/%s",
	"RefSeq": "http://www.ncbi.nlm.nih.gov/nuccore/%s",
	"SABIO-RK": "http://sabio.villa-bosch.de/kineticLawEntry.jsp?kinlawid=%s&viewData=true",
	"SwissProt": IDORG+"uniprot/",
	"Taxonomy": "http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=%s",
	"ThreeDMET": IDORG+"3dmet/",	
	"URL": "%s",
}

import sys
import os.path
import django

from libsbml import *

from django.core.exceptions import ObjectDoesNotExist
django.setup()

from public.models import CrossReference
from public.models import Entry
from public.models import CROSS_REFERENCE_SOURCE_URLS

#read SBML file and get model
reader = SBMLReader()
document = reader.readSBML("test.sbml")
model=document.getModel()

#iterate over all species
for i in range (0,model.getNumSpecies()):
  sp=model.getSpecies(i)
  if not sp.getMetaId():
    sp.setMetaId(sp.getId())
  try:
    o=Entry.objects.get(wid=sp.getId())
    if o.cross_references is not None:
      cv=CVTerm()
      cv.setQualifierType(BIOLOGICAL_QUALIFIER)
      cv.setBiologicalQualifierType(BQB_IS_VERSION_OF)
      for c in o.cross_references.all():
        print CROSS_REFERENCE_SOURCE_URLS[c.source] % c.xid
        cv.addResource(str(CV_SOURCES[c.source]+c.xid))
        sp.addCVTerm(cv)
  except ObjectDoesNotExist:
    print 'does not exist'

#iterate over all reactions
for i in range (0,model.getNumReactions()):
  r=model.getReaction(i)
  if not r.getMetaId():
    r.setMetaId(sp.getId())
  try:
    o=Entry.objects.get(wid=r.getId())
    if o.cross_references is not None:
      cv=CVTerm()
      cv.setQualifierType(BIOLOGICAL_QUALIFIER)
      cv.setBiologicalQualifierType(BQB_IS_VERSION_OF)
      for c in o.cross_references.all():
        print CROSS_REFERENCE_SOURCE_URLS[c.source] % c.xid
        cv.addResource(str(CV_SOURCES[c.source]+c.xid))
        r.addCVTerm(cv)
  except ObjectDoesNotExist:
    print 'does not exist'

writeSBML(document,"test-out.xml");

