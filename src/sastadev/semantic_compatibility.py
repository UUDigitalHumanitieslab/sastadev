import re
from sastadev.NLtypes import Animate, AnyType, Event, Human, Object, SemType, UnKnown, Alt, And
from sastadev.sastatypes import List, SynTree
from sastadev.semtypelexicon import vnwsemdict, wwsemdict, wwreqsemdict, defaultreqsemdict
from sastadev.treebankfunctions import getattval, getheadof


def getsemtype(syntree: SynTree) -> SemType:
    if 'cat' in syntree.attrib:
        hd = getheadof(syntree)                 # do something for coordinations
        result = getsemtype(hd)
    elif 'word' in syntree.attrib:
        result = semlookup(syntree)
    elif 'index' in syntree.attrib:
        antecedent = getantecedentof(syntree)
        result = getsemtype(antecedent)
    else:
        result = UnKnown
    return result

def semlookup(stree: SynTree) -> List[SemType]:
    pt = getattval(stree, 'pt')
    lemma = getattval(stree, 'lemma')
    if pt == 'vnw':
        vnwtype = getattval(stree, 'vwtype')
        pdtype = getattval(stree, 'pdtype')
        if (lemma, vnwtype, pdtype) in vnwsemdict:
            result = vnwsemdict[ (lemma, vnwtype, pdtype)]
        else:
            result = [UnKnown]
    elif pt == 'ww':
        fullframe = getattval(stree, 'frame')
        realframe = fullframe[2]
        if (lemma, realframe) in wwsemdict:
            result = wwsemdict[(lemma, realframe)]
        else:
            result = [Event]
    else:
        result = [UnKnown]
    return result


def semreqlookup(stree: SynTree) -> List[dict]:
    pt = getattval(stree, 'pt')
    lemma = getattval(stree, 'lemma')
    if pt == 'ww':
        fullframe = getattval(stree, 'frame')
        realframe = fullframe[2]
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

def sh(sem: SemType) -> Alt:
    result = Alt([And([sem])])
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