import copy
from sastadev.treebankfunctions import immediately_precedes, showtree
from sastadev.sastatypes import SynTree
from lxml import etree

def transformtreeld(stree:SynTree) -> SynTree:
    debug = False
    if debug:
        showtree(stree, 'intree')
    newstree = copy.deepcopy(stree)
    ldxpath = """.//node[node[@rel="hd" and @pt="ww"] and
       node[@rel="ld" and (@pt="n" or @cat="np")] and
       node[@rel="svp"  and @pt="vz"] and
       not(node[@rel="su"])
       ]"""
    ldclauses = newstree.xpath(ldxpath)
    for ldclause in ldclauses:
        ldnodes = ldclause.xpath(' node[@rel="ld" and (@pt="n" or @cat="np")]')
        if ldnodes != []:
            ldnodes[0].attrib["rel"] = "su"
    if debug:
        showtree(newstree, 'outtree')
    return newstree

def transformtreenogeen(stree:SynTree) -> SynTree:
    debug = False
    if debug:
        showtree(stree, 'intree')
    newstree = copy.deepcopy(stree)
    nogxpath = """.//node[@lemma="nog" and parent::node[not(@cat="np")]]"""
    eenxpath = """.//node[(@lemma="een" or @lemma="één" or @lemma="eentje") and parent::node[@cat="np"]]"""
    nogs = newstree.xpath(nogxpath)
    eens = newstree.xpath(eenxpath)
    for nog in nogs:
        for een in eens:
            if immediately_precedes(nog, een, newstree):
                nog.getparent().remove(nog)
                een.getparent().append(nog)
    if debug:
        showtree(newstree, 'outtree')
    return newstree

def transformtreenogde(stree:SynTree) -> SynTree:
    debug = False
    if debug:
        showtree(stree, 'intree')
    newstree = copy.deepcopy(stree)
    nogxpath = """.//node[@lemma="nog" and parent::node[@cat="np"]]"""
    dexpath = """.//node[(@lemma="de" or @lemma="het" or @lemma="deze" or @lemma="die") and parent::node[@cat="np"]]"""
    nogs = newstree.xpath(nogxpath)
    des = newstree.xpath(dexpath)
    for nog in nogs:
        for de in des:
            if immediately_precedes(nog, de, newstree):
                nog.getparent().remove(nog)
                de.getparent().getparent().append(nog)
    if debug:
        showtree(newstree, 'outtree')
    return newstree