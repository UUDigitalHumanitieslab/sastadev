from typing import List, Tuple
# from sastadev.sastatypes import import DupInfo, Nort
from sastadev.dedup import DupInfo, Nort

def find_commaduplicates2(wl: List[Nort]) -> Tuple[List[Nort], DupInfo]:
    '''
    The function *find_commaduplicates2* identifies each Nort that is immediately followed by a comma and a duplicate,
     or if a comma plus duplicate (popssibly multiple times) are at the end of the utterance.
     It returns a list of these Norts and a dictionary of
    <position of the duplicate: position of its successor> items as the longdups part in
    a DupInfo object.

    '''
    dupmapping = dict()
    result = []
    lwl = len(wl)
    for i in range(lwl - 2):
        if isnortduplicate([wl[i]], [wl[i + 2]]) and iscomma(wl[i+1]):
            duppos = getposition(wl[i])
            origpos = getposition(wl[i + 2])
            dupmapping[duppos] = origpos
            result.append(wl[i])
    alldupinfo = DupInfo(dupmapping, dict())
    return result, alldupinfo

