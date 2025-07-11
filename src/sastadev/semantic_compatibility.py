from lxml import etree
import re
from sastadev.conf import settings
from sastadev.metadata import Meta
from sastadev.methods import MethodName
from sastadev.NLtypes import Animate, AnyType, Event, Human, Object, SemType, UnKnown, Alt, And
from sastadev.sastatypes import List, SynTree
from sastadev.semtypelexicon import sh, vnwsemdict, wwsemdict, wwreqsemdict, defaultreqsemdict
from sastadev.treebankfunctions import getattval, getheadof, getsentence

comma = ','


def getsemheads(stree: SynTree) -> SynTree:
    hds = [child for child in stree if getattval(child, 'rel') in ['hd'] ]  # normal case: hd and nucl
    if hds == []:
        hds = [child for child in stree if getattval(child, 'rel') == 'cnj']  # coordinate structures
    if hds == []:
        cat = getattval(stree, 'cat')                                          # mwus
        if cat == 'mwu':
            mwps = [child for child in stree if getattval(child, 'rel') == 'mwp']
            sortedmwps = sorted(mwps, key=lambda node: int(getattval(node, 'begin')))
            hds = [sortedmwps[0]] if sortedmwps != [] else []
    if hds == []:
        bodies = [child for child in stree if getattval(child, 'rel') in  {'body', 'nucl'} ]  # body, nucl
        thebody = bodies[0] if bodies != [] else None
        if thebody is not None:
            hds = getsemheads(thebody)
        else:
            hds = []
    return hds

def sem_merge(alt1: Alt, alt2: Alt) -> Alt:
    result = Alt(alt1.options + alt2.options)
    return result

def getsemtype(syntree: SynTree) -> SemType:
    if 'cat' in syntree.attrib:
        result = None
        hds = getsemheads(syntree)                 # do something for coordinations, for mwus
        for hd in hds:
            hdresult = getsemtype(hd)
            result  = hdresult if result is None else sem_merge(result, hdresult)
    elif 'word' in syntree.attrib:
        result = semlookup(syntree)
    elif 'index' in syntree.attrib:
        antecedent = getantecedentof(syntree)
        if antecedent is not None:
            result = getsemtype(antecedent)
        else:
            result = sh(UnKnown)
            settings.LOGGER.error(f'No antecedent found for:\n{etree.dump(syntree)} ')
    else:
        result = sh(UnKnown)
    return result

def semlookup(stree: SynTree) -> List[SemType]:
    pt = getattval(stree, 'pt')
    lemma = getattval(stree, 'lemma')
    if pt == 'vnw':
        vnwtype = getattval(stree, 'vwtype')
        pdtype = getattval(stree, 'pdtype')
        if (lemma, pdtype, vnwtype) in vnwsemdict:
            result = vnwsemdict[ (lemma, pdtype, vnwtype)]
        else:
            result = sh(UnKnown)
    elif pt == 'ww':
        fullframe = getattval(stree, 'frame')
        realframe = fullframe[2]
        if (lemma, realframe) in wwsemdict:
            result = wwsemdict[(lemma, realframe)]
        else:
            result = sh(Event)
    else:
        result = sh(UnKnown)
    return result

def getrealframe(fullframe: str) -> str:
    # form = <pos>\(<part> (, <part>)*\)
    lbpos = fullframe.find('(')
    corefullframe = fullframe[lbpos + 1:-1]
    parts = corefullframe.split(comma)
    result = parts[-1] if len(parts) > 0 else ''
    return result
def semreqlookup(stree: SynTree) -> List[dict]:
    pt = getattval(stree, 'pt')
    lemma = getattval(stree, 'lemma')
    if pt == 'ww':
        fullframe = getattval(stree, 'frame')
        realframe = getrealframe(fullframe)
        if (lemma, realframe) in wwreqsemdict:
            result = wwreqsemdict[(lemma, realframe)]
        elif realframe in defaultreqsemdict:
            result = defaultreqsemdict[realframe]
        else:
            result = []
    else:
        result = []
    return result



# propernameframepattern = r"proper\_name\(([A-z]+)\s*\,\s*'([A-z]+)\)"
# def getnameclass(stree: synTree) -> str:
#     # frame proper_name(sg, 'PER')
#     pt = getattval(stree, 'pt')
#     ntype = getattval(stree, 'ntype')
#     lemma = getattval(stree, 'lemma')
#     if pt == 'n':
#         if ntype == 'eigen':
#             frame = getattval(stree, 'frame')
#             nameclass = re.sub(propernameframepattern, r'\2', frame)
#         else:




def getantecedentof(stree: SynTree):
    idx = getattval(stree, 'index')
    antecedentxpath = f'./ancestor::alpino_ds/descendant::node[(@word or @cat) and @index="{idx}"]'
    antecedents = stree.xpath(antecedentxpath)
    if antecedents != []:
        antecedent = antecedents[0]
    else:
        antecedent = None
    return antecedent

def compatible(alt1: Alt, alt2: Alt) -> bool:
    result = altaltcompatible(alt1, alt2)
    return result

def altaltcompatible(alt1: Alt, alt2: Alt):
    for option in alt1.options:
        result = andaltcompatible(option, alt2)
        if result:
            return True
    return False

def andaltcompatible(and1: And, alt2: Alt) -> bool:
    for option in and1.options:
        result = barealtcompatible(option, alt2)
        if result:
            return True
    return False

def barealtcompatible(sem: SemType, alt2: Alt) -> bool:
    for option in alt2.options:
        result = bareandcompatible(sem, option)
        if result:
            return True
    return False

def bareandcompatible(sem: SemType, and2: And) -> bool:
    result = True
    for option in and2.options:
        newresult = barebarecompatible(sem, option)
        result = result and newresult
        if not result:
            return False
    return result

def barebarecompatible(sem1: SemType, sem2: SemType) -> bool:
    if sem1 in {AnyType, UnKnown}:
        return True
    elif sem2 in {AnyType, UnKnown}:
        return True
    elif sem1 == sem2:
        return True
    elif issubclass(sem1, sem2):
        return True
    else:
        return False


wordnodexpath = './/node[@word]'
def semincompatiblecount(stree: SynTree, md:List[Meta], mn:MethodName) -> int:
    sentence = getsentence(stree)        # mainly for debugging ease
    result = 0
    # gather the words
    wordnodes = stree.xpath(wordnodexpath)
    for wordnode in wordnodes:
        wordnodecount = 0
        reqslist = semreqlookup(wordnode)
        if reqslist != []:
            reqslistcounts = []
            for reqs in reqslist:
                reqscount = 0
                parent = wordnode.getparent()
                for sibling in parent:
                    siblingrel = getattval(sibling, 'rel')
                    if siblingrel in reqs:
                        siblingsemtype = getsemtype(sibling)
                        if not compatible(siblingsemtype, reqs[siblingrel]):
                            reqscount += 1
                reqslistcounts.append(reqscount)
            wordnodecount += min(reqslistcounts)
        else:
            pass
        result += wordnodecount
    return result

def mytry():
    pairs = [(Alt([And([Human])]), Alt([And([Object])])),
             (sh(Human), sh(Object)),
             (sh(AnyType), sh(Animate))
             ]
    for alt1, alt2 in pairs:
        result = altaltcompatible(alt1, alt2)
        print(result)

if __name__ == '__main__':
    mytry()