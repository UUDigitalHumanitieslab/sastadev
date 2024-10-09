'''

The module *resultsbyutterance* provides functions to compute the results and the scores per utterance
'''
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

from sastadev.allresults import AllResults
from sastadev.conf import settings
from sastadev.methods import Method
from sastadev.query import query_inform
from sastadev.rpf1 import getscores
from sastadev.sastatypes import GoldResults, QId, ResultsDict, Table, UttId

comma = ','
space = ' '

notapplicable = (0.0, 0.0, 0.0)

byuttheader = ['uttid', 'results', 'bronzeref', 'silverref'] + ['br', 'bp', 'bf1'] + ['sr', 'sp', 'sf1'] + ['utterance']

ResultsByUttDict = Dict[UttId, List[QId]]
ScoresByUttDict = Dict[UttId, List[Tuple[float, float, float]]]


def getresultsbyutt(results: ResultsDict, method: Method) -> ResultsByUttDict:
    resultsbyuttdict: ResultsByUttDict = defaultdict(Counter)
    for reskey in results:
        qid = reskey[0]
        if qid in method.queries:
            thequery = method.queries[qid]
            if query_inform(thequery):
                for uttid in results[reskey]:
                    resultsbyuttdict[uttid].update([reskey])
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
            settings.LOGGER.error(f'No reference data for uttid {uttid}')
    for uttid in reference:
        if uttid not in doneuttids:
            scores[uttid] = notapplicable
            settings.LOGGER.error(f'No results data for uttid {uttid}')
    return scores


def getreference(goldscores: GoldResults) -> ResultsDict:
    reference = {}
    for qid in goldscores:
        reference[qid] = goldscores[qid][2]
    return reference


def getscoresbyutt(results: ResultsDict, refscores: ResultsDict) -> ScoresByUttDict:
    debug = False
    resultsbyutt = getresultsbyutt(results)
    # reference = getreference(goldscores)
    referencebyutt = getresultsbyutt(refscores)
    scoresbyutt = getscoresbyutt2(resultsbyutt, referencebyutt)
    if debug:
        for uttid, triple in scoresbyutt.items():
            print(uttid, triple)
    return scoresbyutt


def mkscoresbyuttrows(allresults: AllResults, bronzerefscores: ResultsDict, silverrefscores: ResultsDict,
                      method: Method) -> Table:
    results = allresults.coreresults
    resultsbyutt = getresultsbyutt(results, method)
    bronzebyutt = getresultsbyutt(bronzerefscores, method)
    silverbyutt = getresultsbyutt(silverrefscores, method)
    bronzescoresbyutt = getscoresbyutt2(resultsbyutt, bronzebyutt)
    silverscoresbyutt = getscoresbyutt2(resultsbyutt, silverbyutt)
    resultsuttids = {uttid for uttid in resultsbyutt}
    bronzeuttids = {uttid for uttid in bronzebyutt}
    silveruttids = {uttid for uttid in silverbyutt}
    alluttids = resultsuttids.union(bronzeuttids.union(silveruttids))
    alluttidlist = list(alluttids)
    sortedalluttidlist = sorted(alluttidlist, key=lambda x: int(x))
    rows = []
    for uttid in sortedalluttidlist:
        if uttid in resultsuttids:
            results = counter2str(resultsbyutt[uttid], method)
        else:
            results = ''
        if uttid in bronzebyutt:
            bronzeref = counter2str(bronzebyutt[uttid], method)
        else:
            bronzeref = ''
        if uttid in silverbyutt:
            silverref = counter2str(silverbyutt[uttid], method)
        else:
            silverref = ''
        if uttid in bronzescoresbyutt:
            r, p, f1 = bronzescoresbyutt[uttid]
            bronzescores = [r, p, f1]
        else:
            r, p, f1 = notapplicable
            bronzescores = [r, p, f1]
        if uttid in silverscoresbyutt:
            r, p, f1 = silverscoresbyutt[uttid]
            silverscores = [r, p, f1]
        else:
            r, p, f1 = notapplicable
            silverscores = [r, p, f1]
        utt = space.join(allresults.allutts[uttid]) if uttid in allresults.allutts else '@@'
        fullrow = [uttid, results, bronzeref, silverref] + bronzescores + silverscores + [utt]
        rows.append(fullrow)
    return rows

def counter2itemlist(scores: Counter, method: Method) -> List[str]:
    resultlist = []
    for reskey in scores:
        qid = reskey[0]
        thequery = method.queries[qid]
        theitem = thequery.item if reskey[0] == reskey[1] else f'{thequery.item}={reskey[1]}'
        sublist = scores[reskey] * [theitem]
        resultlist += sublist
    sortedresultlist = sorted(resultlist)
    return sortedresultlist

def counter2str(scores: Counter, method: Method) -> str:
    resultlist = counter2itemlist(scores, method)
    result = comma.join(resultlist)
    return result