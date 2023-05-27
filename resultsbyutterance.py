'''

The module *resultsbyutterance* provides functions to compute the results and the scores per utterance
'''
from typing import Dict, List, Tuple
from sastatypes import ResultsDict, UttId, QId
from collections import defaultdict
from rpf1 import getscores
from config import SDLOGGER
from collections import Counter
from sastatypes import ResultsDict, GoldResults

notapplicable = (0.0, 0.0, 0.0)

ResultsByUttDict = Dict[UttId, List[QId]]
ScoresByUttDict = Dict[UttId, List[Tuple[float, float, float]]]


def getresultsbyutt(results: ResultsDict) -> ResultsByUttDict:
    resultsbyuttdict : ResultsByUttDict = defaultdict(Counter)
    for qid in results:
        for uttid in results[qid]:
            resultsbyuttdict[uttid].update([qid])
    return resultsbyuttdict

def getscoresbyutt2(results: ResultsByUttDict, reference: ResultsByUttDict) -> ScoresByUttDict:
    scores = {}
    doneuttids = []
    for uttid in results:
        doneuttids.append(uttid)
        if uttid in reference:
            scores[uttid] = getscores(results[uttid], reference[uttid])
        else:
            scores[uttid] = notapplicable
            SDLOGGER.error(f'No reference data for uttid {uttid}')
    for uttid in reference:
        if uttid not in doneuttids:
            scores[uttid] = notapplicable
            SDLOGGER.error(f'No results data for uttid {uttid}')
    return scores

def getreference(goldscores: GoldResults) -> ResultsDict:
    reference = {}
    for qid in goldscores:
         reference[qid] = goldscores[qid][2]
    return reference


def getscoresbyutt(results: ResultsDict, goldscores: GoldResults) -> ScoresByUttDict:
    debug = True
    resultsbyutt = getresultsbyutt(results)
    reference = getreference(goldscores)
    referencebyutt = getresultsbyutt(reference)
    scoresbyutt = getscoresbyutt2(resultsbyutt, referencebyutt)
    if debug:
        for uttid, triple in scoresbyutt.items():
            print(uttid, triple)
    return scoresbyutt
