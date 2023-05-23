'''

The module *resultsbyutterance* provides functions to compute the results and the scores per utterance
'''
from collections import defaultdict
from typing import Dict, List

from sastadev.sastatypes import QId, ResultsDict, UttId

ResultsByUttDict = Dict[UttId, List[QId]]


def getresultsbyutt(results: ResultsDict) -> ResultsByUttDict:
    resultsbyuttdict : ResultsByUttDict = defaultdict(list)
    for qid in results:
        for uttid in results[qid]:
            resultsbyuttdict[uttid].append(qid)
    return resultsbyuttdict

