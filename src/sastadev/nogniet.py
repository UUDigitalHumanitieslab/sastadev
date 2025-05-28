import copy
from sastadev.sastatypes import SynTree
from sastadev.treebankfunctions import find1


nognietxpath = """.//node[@cat="advp" and node[@rel="mod" and @lemma="nog"] and node[@rel="hd" and @lemma="niet"]]"""
zelfinnpmodxpath = """.//node[@rel="mod" and @lemma="zelf" and parent::node[@cat="np"]]"""

def nognietsplit(stree: SynTree) -> SynTree:
    newstree = copy.deepcopy(stree)
    nognietnodes = newstree.xpath(nognietxpath)
    if nognietnodes == []:
        return stree
    for nognietnode in nognietnodes:
        nog = find1(nognietnode, """./node[@lemma="nog"]""")
        nognietnodeparent = nognietnode.getparent()
        nognietnode.remove(nog)
        for i, anode in enumerate(nognietnodeparent):
            if anode == nognietnode:
                nognietnodepos = i
                break
        nognietnodeparent[i] = nognietnode
    return newstree


def ikzelfsplit(stree: SynTree) -> SynTree:
    newstree = copy.deepcopy(stree)
    zelfinnps = newstree.xpath(zelfinnpmodxpath)
    if zelfinnps == []:
        return stree
    for zelfinnp in zelfinnps:
        npnode = zelfinnp.getparent()
        npparentnode = npnode.getparent()





