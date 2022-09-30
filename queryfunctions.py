from macros import expandmacros
from treebankfunctions import get_left_siblings, getattval, parent, find1, adjacent

from typing import Callable, List
from sastatypes import SynTree


nietxpath = './/node[@lemma="niet"]'
wordxpath = './/node[@pt]'

vzn1basexpath = './/node[ @cat="pp" and (node[@pt="vz"] and node[(@pt="n" or @pt="vnw") and not (%Rpronoun%) and @rel="obj1"] and not(node[@pt="vz" and @vztype="fin"]))]'
vzn1xpath = expandmacros(vzn1basexpath)
vzn2xpath = './/node[node[@lemma="in" and @rel="mwp"] and node[@lemma="deze" and @rel="mwp"]]'
vzn3xpath = './/node[@pt="vz" and ../node[(@lemma="dit" or @lemma="dat")  and @begin>=../node[@pt="vz"]/@end and count(node)<=3] ]'
#vzn4basexpath = './/node[node[@pt="vz" and @rel="hd" and ../node[%Rpronoun% and @rel="obj1" and @end <= ../node[@rel="hd"]/@begin]]]'
#vzn4xpath = expandmacros(vzn4basexpath)


voslashbijxpath = expandmacros(""".//node[node[@pt="vz" and @rel="hd"] and 
            node[@rel="obj1" and 
                 ((@index and not(@word or @cat)) or
                  (%Rpronoun%)
                 )]]""")
vobijxpath = expandmacros('.//node[%Vobij%]')

notadjacent = lambda n1, n2, t: not adjacent(n1, n2, t)


def xneg(stree):
    nodepairs = []
    nietnodes = stree.xpath(nietxpath)
    for nietnode in nietnodes:
        pnietnode = parent(nietnode)
        leftnietsiblings = get_left_siblings(nietnode)
        leftsiblings = get_left_siblings(pnietnode)
        ppnietnode = parent(pnietnode)
        if getattval(pnietnode, 'cat') == "advp" and len(leftsiblings) == 1 and getattval(ppnietnode, 'rel') == '--':
            result = True
            theleftsibling = leftsiblings[0]
        elif getattval(pnietnode, 'cat') != "advp" and getattval(pnietnode, 'rel') == '--' and len(leftnietsiblings) == 1:
            result = True
            theleftsibling = leftnietsiblings[0]
        else:
            result = False
        if result:
            nodepairs.append((theleftsibling, nietnode))
    if nodepairs == []:
        return None
    else:
        return nodepairs[0]


def xneg_neg(stree):
    (x, neg) = xneg(stree)
    return neg


def xneg_x(stree):
    (x, neg) = xneg(stree)
    return x


def VzN(stree):
    results = []
    results += stree.xpath(vzn1xpath)
    results += stree.xpath(vzn2xpath)
    results += stree.xpath(vzn3xpath)
    #results += stree.xpath(vzn4xpath) # does not belong here after all, these will be scored under Vo/Bij
    return results

def auxvobij(stree: SynTree, pred: Callable[[SynTree, SynTree, SynTree], bool]):
    RPnodes = stree.xpath(voslashbijxpath)
    results = []
    for RPnode in RPnodes:
        # find the head node
        headnode = find1(RPnode, 'node[@rel="hd"]')

        # find the obj1node
        obj1node = find1(RPnode, 'node[@rel="obj1"]')

        # check if they are adjacent
        if headnode is not None and obj1node is not None:
            if pred(headnode, obj1node, stree):
                results.append(RPnode)
    return results


def vobij(stree: SynTree) -> List[SynTree]:
    results1 = stree.xpath(vobijxpath)
    results2 = auxvobij(stree, adjacent)
    results = results1 + results2
    return results


def voslashbij(stree: SynTree) -> List[SynTree]:
    results = auxvobij(stree, notadjacent)
    return results
