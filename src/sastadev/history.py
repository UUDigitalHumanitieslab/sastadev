from collections import defaultdict, Counter
from dataclasses import dataclass
from sastadev.basicreplacements import innereplacements, innureplacements
from sastadev.CHAT_Annotation import CHAT_explanation, CHAT_replacement, CHAT_wordnoncompletion
from sastadev.cleanCHILDEStokens import cleantext
from sastadev.readcsv import readcsv
from sastadev.conf import settings
from sastadev.sastatypes import TreeBank
from sastadev.treebankfunctions import getorigutt, getyield, getxselseuttid
import os

childescorrectionsfullname = os.path.join(settings.SD_DIR, 'data', 'childescorrections', 'childescorrections.txt')

@dataclass
class HistoryCorrection:
    wrong: str
    correction: str
    correctiontype: str
    frequency: int


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


def getchildescorrections(filename) -> defaultdict:
    resultdict = defaultdict(list)
    idata = readcsv(filename, header=False)
    for i, row in idata:
        wrong = row[0]
        newhc = HistoryCorrection(wrong=wrong, correction=row[1], correctiontype=row[2], frequency=int(row[3]))
        resultdict[wrong].append(newhc)

    return resultdict

childescorrections = getchildescorrections(childescorrectionsfullname)
childescorrectionsexceptions = ['nie', 'moe', 'dee', 'ie', 'su', 'an', 'tan'] + \
                               [tpl[0] for tpl in innereplacements] + \
                               [tpl[0] for tpl in innureplacements]