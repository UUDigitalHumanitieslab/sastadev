'''
defines functions for the STAP post part of the methods

'''
from collections import Counter

from sastadev.allresults import mkresultskey
from sastadev.rpf1 import sumfreq
from sastadev.sastatypes import QId
from typing import List

BB_ids = ['S010', 'S011', 'S012']
S013qid = 'S013'
S013reskey = mkresultskey(S013qid)


def BB_totaal(allresults, _):
    scores = []
    for qid in BB_ids:
        if qid in allresults.coreresults:
            scores.append(allresults.coreresults[qid])
        else:
            scores.append(Counter())
    counts = [len(s) for s in scores]
    result = sum(counts)
    return result


def GLVU(allresults, _):
    total_length_VU = 0
    if S013reskey in allresults.coreresults:
        for key in allresults.coreresults[S013reskey]:
            total_length_VU += allresults.coreresults[S013reskey][key]
    result = total_length_VU / allresults.uttcount
    return result


def GL5LVU(allresults, _):
    counts = []
    if S013reskey in allresults.coreresults:
        for key in allresults.coreresults[S013reskey]:
            counts.append(allresults.coreresults[S013reskey][key])
    sorted_counts = counts.sort()
    result = sum(counts[45:50]) / 5
    return result

overige_fouten_qids =['S026', 'S027', 'S028', 'S029', 'S030', 'S031', 'S032', 'S033',]
def overige_fouten_count(allresults, _) -> int:
    result = fouten_count(overige_fouten_qids, allresults)
    return result

congruentie_fouten_qids = ['S022', 'S034', 'S035']
def congruentie_fouten_count(allresults, _) -> int:
    result = fouten_count(congruentie_fouten_qids, allresults)
    return result

bepaler_verkeerd_qids = ['S021', 'S037']
def bepaler_verkeerd_count(allresults, _) -> int:
    result = fouten_count(bepaler_verkeerd_qids, allresults)
    return result

bepaler_weg_qids = ['S020']
def bepaler_weg_count(allresults, _) -> int:
    result = fouten_count(bepaler_weg_qids, allresults)
    return result

def fouten_count(qids: List[QId], allresults) -> int:
    result = 0
    for qid in qids:
        reskey = mkresultskey(qid)
        if reskey in allresults.coreresults:
            result += sumfreq(allresults.coreresults[reskey])
    return result


