from treebankfunctions import getattval, getnodeyield
from sastadev.sastatypes import SynTree
from typing import List

def isdet(node) -> bool:
    nodept = getattval(node, 'pt')
    nodepdtype = getattval(node, pdtype)
    result = nodept in ['lw'] or (nodept in  ['vnw'] nodepdtype in ['det']
    return result


def contentword(node) -> bool:
    nodept = getattval(node, 'pt')
    result = nodept in ['n', 'ww', 'adj', 'bw']
    return result

token2nodemap = {}
tokens = []
newtokens = []
naarfound = False

for i, token in enumerate(tokens):
    naarfound = token.word == 'naar'
    if not naarfound:
        if i + 2 < len(tokens) and tokens[i].pos in token2nodemap and \
                tokens[i+1].pos in token2nodemap and \
                tokens[i+2].word == 'toe':
            thisnode = token2nodemap[i]
            nextnode = token2nodemap[i+1]
            if isdet(thisnode) and contentword(nextnode):
                naartoken = mktoken('naar')
                naarfound = True
                newtokens.append(naartoken)
        elif i +1 < len(tokens) and tokens[i].pos in token2nodemap and \
                tokens[i+1].word == 'toe':
            thisnode = token2nodemap[i]
            if contentword(thisnode):
                naartoken = mktoken('naar')
                naarfound = True
                newtokens.append(naartoken)
    else:
        newtokens.append(token)

def isvariantcompatible(variant: str, variants:str) -> bool:
    rawvariantlist = variants.split(comma)
    variantlist = [variant.strip() for variant in rawvariantlist]
    result = variantlist == [] or variant in variantlist
    return result

import copy
def transformtree(stree:SynTree) -> SynTree:
    newstree = copy.deepcopy(stree)
    ldxpath = """.//node[node[@rel="hd" and @pt="ww"] and
       node[@rel="ld" and (@pt="n" or @cat="np")] and
       node[@rel="svp"  and @pt="vz"] and
       not(node[@rel="su"])
       ]"""
    ldclauses = stree.xpath(ldxpath)
    for ldclause in ldclauses:
        ldnode = ldclause.xpath(' node[@rel="ld" and (@pt="n" or @cat="np")]')
        ldnode.attrib["rel"] = "su"
    return newstree