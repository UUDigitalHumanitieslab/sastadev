from collections import Counter
from treebankfunctions import getattval, getuttid, getnodeyield
from stringfunctions import realwordstring
from copy import deepcopy
from lexicon import getwordposinfo, getwordinfo

lpad = 3
zero = '0'
astamaxwordcount = 300

excluded_lemmas = ['gevallen', 'gewinnen']

nounqid = 'A021'
lexqid = 'A018'
samplesizeqid = 'A045'
mluxqid = 'A029'
pvqid = 'A024'
delpvqid = 'A009'
subpvqid = 'A032'
kqid = 'A013'
mqid = 'A020'
tijdfoutpvqid = 'A041'
nounlemmaqid = 'A046'
verblemmaqid = 'A049'

specialform = 'Special Form'
errormarking  = 'Error Marking'

mdnamemdxpathtemplate = """.//xmeta[@name="{mdname}" and @value="{mdvalue}"]"""
ptposxpathtemplate = './/node[@pt and @begin="{position}"]'


def mdbasedquery(stree, mdname, mdvalue):
    mdnamemdxpath = mdnamemdxpathtemplate.format(mdname=mdname, mdvalue=mdvalue)
    mdnamemds = stree.xpath(mdnamemdxpath)
    results = []
    for mdnamemd in mdnamemds:
        annotatedposstr = mdnamemd.attrib['annotatedposlist']
        if annotatedposstr != '':
            mdbeginval = annotatedposstr[1:-1]
            ptposxpath = ptposxpathtemplate.format(position=mdbeginval)
            newresults = stree.xpath(ptposxpath)
            results += newresults

    return results

def neologisme(stree):
    results1 = mdbasedquery(stree, errormarking,"['n']")
    results2 = mdbasedquery(stree, specialform, '@n')
    results = results1 + results2
    return results

def sempar(stree):
    results = mdbasedquery(stree, errormarking, "['s']")
    return results

def phonpar(stree):
    results = mdbasedquery(stree, errormarking, "['p']")
    return results




def sumctr(ctr):
    result = sum(ctr.values())
    return result


def wordcountperutt(allresults):
    lemmas = getalllemmas(allresults)
    wordcounts = {uttid: sum(ctr.values()) for uttid, ctr in lemmas.items()}
    ignorewordcounts = deepcopy(
        allresults.coreresults[samplesizeqid]) if samplesizeqid in allresults.coreresults else Counter()  # samplesize
    ignorewordcounts += allresults.coreresults[mluxqid] if mluxqid in allresults.coreresults else Counter()  # mlux
    # ignorewordcounts += allresults.coreresults['A050'] if 'A050' in allresults.coreresults else Counter() # echolalie covered by mlux
    result = {}
    for uttid in wordcounts:
        tosubtract = ignorewordcounts[uttid] if uttid in ignorewordcounts else 0
        result[uttid] = wordcounts[uttid] - tosubtract
    # remove uttids which have 0 words
    result = {uttid: ctr for uttid, ctr in result.items() if ctr != 0}
    return result


def finietheidsindex(allresults, _):
    allpvs = allresults.coreresults[pvqid] if pvqid in allresults.coreresults else Counter()
    subpvs = allresults.coreresults[subpvqid] if subpvqid in allresults.coreresults else Counter()
    delpvs = allresults.coreresults[delpvqid] if delpvqid in allresults.coreresults else Counter()
    tijdfoutpvs = allresults.coreresults[tijdfoutpvqid] if tijdfoutpvqid in allresults.coreresults else Counter()
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
    # @@to be adapted
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
    Kcount = sumctr(allresults.coreresults[kqid]) if kqid in allresults.coreresults else 0
    Mcount = sumctr(allresults.coreresults[mqid]) if mqid in allresults.coreresults else 0
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
    result = getcondlemmas(allresults, _, lambda qid: qid in [nounqid, lexqid])
    return result


def getnounlemmas(allresults, _):
    result = getposlemmas(allresults, nounqid)
    return result


def getlexlemmas(allresults, _):
    result = getposlemmas(allresults, lexqid)
    return result


def realword(node):
    result = getattval(node, 'pt') not in ['let']
    return result


def getalllemmas(allresults):
    result = {}
    if allresults.annotationinput:
        for uttid in allresults.allutts:
            lemmas = [bgetlemma(w) for w in allresults.allutts[uttid] if realwordstring(w)]
            result[uttid] = Counter(lemmas)
    else:
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


def oldgetcondlemmas(allresults, _, cond):
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

#not used anymore, contains an error
def getcondlemmas(allresults, _, cond):
    result = Counter()
    if allresults.annotationinput:
        for qid in allresults.exactresults:
            if cond(qid):
                for (uttid, position) in allresults.exactresults[qid]:
                    word = allresults.allutts[uttid][position - 1]
                    if qid == 'A021':
                        pos = 'n'
                    elif qid == 'A018':
                        pos = 'ww'
                    else:
                        pos = None
                    lemma = bgetlemma(word, pos)
                    result.update([(lemma, qid, uttid)])

    else:
        allmatches = allresults.allmatches
        for el in allmatches:
            (qid, uttid) = el
            if cond(qid):
                for amatch in allmatches[el]:
                    # theword = normalizedword(amatch[0])
                    theword = getattval(amatch[0], 'lemma')
                    result.update([(theword, uttid)])
    return result


def getposfromqid(qid):
    if qid == 'A021':
        pos = 'n'
    elif qid == 'A018':
        pos = 'ww'
    else:
        pos = None
    return pos


def getposlemmas(allresults, posqid):
    result = Counter()
    if allresults.annotationinput:
        for (uttid, position) in allresults.exactresults[posqid]:
            word = allresults.allutts[uttid][position - 1]
            pos = getposfromqid(posqid)
            lemma = bgetlemma(word, pos)
            result.update([(lemma, uttid)])
    else:
        allmatches = allresults.allmatches
        for el in allmatches:
            (qid, uttid) = el
            if qid == posqid:
                for amatch in allmatches[el]:
                    # theword = normalizedword(amatch[0])
                    theword = getattval(amatch[0], 'lemma')
                    result.update([(theword, uttid)])
    return result


def bgetlemma(word, pos=None):
    if pos is None:
        wordinfos = getwordinfo(word)
        if wordinfos == []:
            lemma = word
        else:
            filteredwordinfos = [wi for wi in wordinfos if wi[3] not in excluded_lemmas]
            if filteredwordinfos == []:
                lemma = wordinfos[0][3]
            else:
                lemma = filteredwordinfos[0][3]
    else:
        wordinfos = getwordposinfo(word, pos)
        if wordinfos == []:
            lemma = word
        else:
            filteredwordinfos = [wi for wi in wordinfos if wi[3] not in excluded_lemmas]
            if filteredwordinfos == []:
                lemma = wordinfos[0][3]
            else:
                lemma = filteredwordinfos[0][3]
    return lemma
