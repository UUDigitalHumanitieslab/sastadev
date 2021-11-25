from collections import Counter
from copy import deepcopy

from treebankfunctions import getattval, getnodeyield, getuttid

lpad = 3
zero = '0'
astamaxwordcount = 300


def sumctr(ctr):
    result = sum(ctr.values())
    return result


def wordcountperutt(allresults):
    lemmas = getalllemmas(allresults)
    wordcounts = {uttid: sum(ctr.values()) for uttid, ctr in lemmas.items()}
    ignorewordcounts = deepcopy(allresults.coreresults['A045']) if 'A045' in allresults.coreresults else Counter()  # samplesize
    ignorewordcounts += allresults.coreresults['A029'] if 'A029' in allresults.coreresults else Counter()  # mlux
    # ignorewordcounts += allresults.coreresults['A050'] if 'A050' in allresults.coreresults else Counter() # echolalie covered by mlux
    result = {}
    for uttid in wordcounts:
        tosubtract = ignorewordcounts[uttid] if uttid in ignorewordcounts else 0
        result[uttid] = wordcounts[uttid] - tosubtract
    # remove uttids which have 0 words
    result = {uttid: ctr for uttid, ctr in result.items() if ctr != 0}
    return result


def finietheidsindex(allresults, _):
    allpvs = allresults.coreresults['A024'] if 'A024' in allresults.coreresults else Counter()
    subpvs = allresults.coreresults['A032'] if 'A032' in allresults.coreresults else Counter()
    delpvs = allresults.coreresults['A009'] if 'A009' in allresults.coreresults else Counter()
    tijdfoutpvs = allresults.coreresults['A041'] if 'A041' in allresults.coreresults else Counter()
    foutepvs = subpvs + delpvs + tijdfoutpvs
    allpvcount = sumctr(allpvs)
    foutepvcount = sumctr(foutepvs)
    okpvcount = allpvcount - foutepvcount
    if allpvcount == 0:
        result = 0
    else:
        result = okpvcount / allpvcount
    return result


def countwordsandcutoff(allresults, _):
    result = (None, 0)
    if 'A047' in allresults.postresults:
        paddedlist = []
        for key, val in allresults.postresults['A047'].items():
            paddedkey = key.rjust(lpad, zero)
            paddedlist.append((paddedkey, val))
        sortedlist = sorted(paddedlist)
        wc = 0
        for key, val in sortedlist:
            if wc + val > astamaxwordcount:
                result = (key, wc)
                break
            else:
                wc += val
                result = (None, wc)
    return result


def KMcount(allresults, _):
    Kcount = sumctr(allresults.coreresults['A013']) if 'A013' in allresults.coreresults else 0
    Mcount = sumctr(allresults.coreresults['A020']) if 'A020' in allresults.coreresults else 0
    result = Kcount + Mcount
    return result


def old_old_getlemmas(allresults, _):
    allmatches = allresults.allmatches
    allresults.postresults['A046'] = Counter()
    for el in allmatches:
        (qid, uttid) = el
        if qid in ['A021', 'A018']:
            for amatch in allmatches[el]:
                # theword = normalizedword(amatch[0])
                theword = getattval(amatch[0], 'lemma')
                allresults.postresults['A046'].update([(theword, uttid)])
    return allresults


def getlemmas(allresults, _):
    result = getcondlemmas(allresults, _, lambda qid: qid in ['A021', 'A018'])
    return result


def realword(node):
    result = getattval(node, 'pt') not in ['let']
    return result


def getalllemmas(allresults):
    result = {}
    for syntree in allresults.analysedtrees:
        uttid = getuttid(syntree)
        lemmas = [getattval(node, 'lemma') for node in getnodeyield(syntree) if realword(node)]
        result[uttid] = Counter(lemmas)
    return result


def old_getlemmas(allresults, _):
    allmatches = allresults.allmatches
    result = Counter()
    for el in allmatches:
        (qid, uttid) = el
        if qid in ['A021', 'A018']:
            for amatch in allmatches[el]:
                # theword = normalizedword(amatch[0])
                theword = getattval(amatch[0], 'lemma')
                result.update([(theword, uttid)])
    return result


def getcondlemmas(allresults, _, cond):
    allmatches = allresults.allmatches
    result = Counter()
    for el in allmatches:
        (qid, uttid) = el
        if cond(qid):
            for amatch in allmatches[el]:
                # theword = normalizedword(amatch[0])
                theword = getattval(amatch[0], 'lemma')
                result.update([(theword, uttid)])
    return result
