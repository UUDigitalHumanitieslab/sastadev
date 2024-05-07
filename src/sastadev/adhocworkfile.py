from typing import List, Tuple
from sastadev.dedup import isnortduplicate, getposition, DupInfo, Nort
from sastadev.sastatypes import Node, Token
from sastadev.treebankfunctions import getattval

comma = ','

def find_simplecommaduplicates2(wl: List[Nort]) -> Tuple[List[Nort], DupInfo]:
    '''
    The function *find_simplecommaduplicates2* identifies each Nort that is followed by a comma and a duplicate of
    itself. It returns a list of these (Nort, commaNort) pairs and a dictionary of
    <position of the duplicate: positions of its successor> items as the commalongdups part in
    a DupInfo object.

    '''
    dupmapping = dict()
    result = []
    lwl = len(wl)
    for i in range(lwl - 2):
        if isnortduplicate([wl[i]], [wl[i + 2]]) and iswordnort(wl[i+1], comma):
            duppos = (getposition(wl[i]), getposition(wl[i+1]))
            origpos = getposition(wl[i + 2])
            dupmapping[duppos] = origpos
            result.append((wl[i], wl[i+1]))
    alldupinfo = DupInfo(dupmapping, dict())
    return result, alldupinfo

def iswordnort(nort: Nort, wrd: str):
    if nort is None:
        result = False
    elif isinstance(nort, Token):
        result = nort.word == wrd
    elif isinstance(nort, Node):
        result = getattval(nort, 'word') == wrd
    else:
        result = False
    return result