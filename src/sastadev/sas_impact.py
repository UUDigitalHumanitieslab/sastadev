from collections import Counter
import copy
from sastadev.allresults import AllResults
from sastadev.methods import Method
from sastadev.rpf1 import getscores, getevalscores
from sastadev.resultsbyutterance import getresultsbyutt, getscoresbyutt2
from typing import Dict, List, Tuple

def sas_impact(allresults: AllResults, silverrefscores, method: Method):
    # maximum nuber of utterances to be reviewed
    n = 10
    f1target = 95

    results = allresults.coreresults
    resultsbyutt = getresultsbyutt(results, method)
    silverbyutt = getresultsbyutt(silverrefscores, method)
    silverscoresbyutt = getscoresbyutt2(resultsbyutt, silverbyutt)

    # reverse sort them by silver F1
    silverscorebyuttlist = [(uttid, score) for uttid, score in silverscoresbyutt.items()]
    sortedsilverscorebyutt = sorted(silverscorebyuttlist, key= lambda x: x[1][2])

    resultscount, refcount, intersectioncount = getcomparisoncounts(resultsbyutt, silverbyutt)
    originalscores = getevalscores(resultscount, refcount, intersectioncount)

    sasresultsbyutt = copy.deepcopy(resultsbyutt)
    allscores = [originalscores]
    for i in range(n):

        # change the results to the silver reference
        curruttid = sortedsilverscorebyutt[i][0]
        sasresultsbyutt[curruttid] = silverbyutt[curruttid]

        # compute the overall score
        resultscount, refcount, intersectioncount = getcomparisoncounts(sasresultsbyutt, silverbyutt)
        newscores = getevalscores(resultscount, refcount, intersectioncount)
        allscores.append(newscores)
        if newscores[2] >= f1target:
            break
    return allscores


def mksas_impactrows(allscores: List[Tuple[float]], not100count:int) -> List[str]:
    # a list of the F1 scores, plus a header
    row = [score[2] for score in allscores]
    lrow = len(row) - 1
    header = ['not100count', 'original'] + [f'{str(i+1)} utts reviewed' for i in range(lrow)]
    rows = [[not100count] + row]
    return header, rows


def getcomparisoncounts(results: Dict[str, Counter], reference: Dict[str, Counter]) -> Tuple[int, int, int]:
   resultscount = 0
   referencecount = 0
   intersectioncount = 0

   for key in results:
       resultscount += sum(results[key].values())

   for key in reference:
       referencecount += sum(reference[key].values())

   for key in results:
       if key in reference:
           intersection = results[key] & reference[key]
           intersectioncount += sum(intersection.values())
   return resultscount, referencecount, intersectioncount
