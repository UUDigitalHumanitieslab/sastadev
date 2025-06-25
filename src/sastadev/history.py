import copy
import os
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

from sastadev.basicreplacements import innereplacements, innureplacements
from sastadev.CHAT_Annotation import (CHAT_explanation, CHAT_replacement,
                                      CHAT_wordnoncompletion)
from sastadev.cleanCHILDEStokens import cleantext
from sastadev.conf import settings
from sastadev.readcsv import readcsv, writecsv
from sastadev.sastatypes import TreeBank
from sastadev.treebankfunctions import getorigutt, getxselseuttid, getyield

childescorrectionspath = os.path.join(settings.SD_DIR, 'data', 'childescorrections')

childescorrectionsfullname = os.path.join(childescorrectionspath, 'childescorrections.txt')
samplecorrectionsfullname = os.path.join(childescorrectionspath, 'samplecorrections.txt')
donefilesfullname = os.path.join(childescorrectionspath, 'donefiles.txt')

@dataclass
class HistoryCorrection:
    wrong: str
    correction: str
    correctiontype: str
    frequency: int

HistoryCorrectionDict = Dict[str, List[HistoryCorrection]]
space = ' '
eps = ''

correctionset = [CHAT_explanation, CHAT_replacement, CHAT_wordnoncompletion]

chatshorttypedict = {CHAT_explanation: 'explanation',
                     CHAT_wordnoncompletion: 'noncompletion',
                     CHAT_replacement: 'replacement'}


def getshortchattype(metaname: str) -> str:
    if metaname in chatshorttypedict:
        return chatshorttypedict[metaname]
    else:
        return 'unknown'


def gathercorrections(treebank: TreeBank) -> defaultdict:
    resultlist = []
    resultdict = defaultdict(list)
    frqcounter = Counter()
    for stree in treebank:
        origutt = getorigutt(stree)
        if origutt is None:
            uttid = getxselseuttid(stree)
            settings.LOGGER.error('Missing origutt in utterance {}'.format(uttid))
            origutt = space.join(getyield(stree))

        _, chatmetadata = cleantext(origutt, False, tokenoutput=True)
        for meta in chatmetadata:
            if meta.name in correctionset:
                wrong = eps.join(meta.annotatedwordlist)
                correct = space.join(meta.annotationwordlist)
                corrtype = getshortchattype(meta.name)
                resultlist.append((wrong, correct, corrtype))

    frqcounter.update(resultlist)

    for (wrong, correct, corrtype) in frqcounter:
        frq = frqcounter[(wrong, correct, corrtype)]
        newhc = HistoryCorrection(wrong=wrong, correction=correct, correctiontype=corrtype, frequency=frq)
        resultdict[wrong].append(newhc)
    return resultdict


def getcorrections(filename) -> defaultdict:
    resultdict = defaultdict(list)
    idata = readcsv(filename, header=False)
    for i, row in idata:
        wrong = row[0]
        newhc = HistoryCorrection(wrong=wrong, correction=row[1], correctiontype=row[2], frequency=int(row[3]))
        resultdict[wrong].append(newhc)

    return resultdict


def getdonefilenames(filename) -> set:
    result = set()
    idata = readcsv(filename, header=False)
    for i, row in idata:
        result.add(row[0])
    return result

def putdonefilenames(donefiles: set, filename):
    data = []
    for el in donefiles:
        data.append([el])
    writecsv(data, filename)

def putcorrections(corrections, filename):
    data = []
    for wrong in corrections:
        hcs = corrections[wrong]
        for hc in hcs:
            row = [wrong, hc.correction, hc.correctiontype, hc.frequency]
            data.append(row)
    writecsv(data, filename)

def remove(lst, togo) -> list:
    newlst = []
    for el in lst:
        if el != togo:
            newlst.append(el)
    return newlst

def mergecorrections(corrections1: HistoryCorrectionDict, corrections2: HistoryCorrectionDict) \
        -> HistoryCorrectionDict:
    largest = corrections1 if len(corrections1) >= len(corrections2) else corrections2
    smallest = corrections1 if len(corrections1) < len(corrections2) else corrections2
    resultdict = copy.deepcopy(largest)
    for wrd in smallest:
        if wrd not in resultdict:
            resultdict[wrd] = smallest[wrd]
        else:
            hcs1 = smallest[wrd]
            hcs2 = resultdict[wrd]
            newhcs = []
            hc1stodo = [hc for hc in hcs1]
            hc2stodo = [hc for hc in hcs2]
            for hc1 in hcs1:
                for hc2 in hcs2:
                    if hc1 in hc1stodo and hc2 in hc2stodo and \
                            hc1.correction == hc2.correction and hc1.correctiontype == hc2.correctiontype:
                        newhc = HistoryCorrection(hc1.wrong, hc1.correction, hc1.correctiontype,
                                                  hc1.frequency + hc2.frequency)
                        newhcs.append(newhc)
                        hc1stodo = remove(hc1stodo, hc1)
                        hc2stodo = remove(hc2stodo, hc2)
            newhcs = newhcs + hc1stodo + hc2stodo
            resultdict[wrd] = newhcs
    return resultdict

childescorrections = getcorrections(childescorrectionsfullname)
childescorrectionsexceptions = ['nie', 'moe', 'dee', 'ie', 'su', 'an', 'tan', 'dees', 'tu'] + \
                               [tpl[0] for tpl in innereplacements] + \
                               [tpl[0] for tpl in innureplacements]

samplecorrections = getcorrections(samplecorrectionsfullname)
donefiles = getdonefilenames(donefilesfullname)
