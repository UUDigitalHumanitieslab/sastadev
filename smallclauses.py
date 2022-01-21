from config import SDLOGGER
from treebankfunctions import getstree, getnodeyield, getattval
from dedup import filledpauseslexicon
from top3000 import ishuman, transitive, intransitive, pseudotr, isanimate, genlexicon
from lexicon import known_word
from namepartlexicon import namepart_isa_namepart
from sastatoken import Token, show
from tokenmd import TokenListMD
from metadata import Meta, bpl_delete, defaultpenalty, insertion, smallclause, SASTA, bpl_none, tokenmapping,\
    insertiontokenmapping

space = ' '
biglocvzs = ['achter', 'beneden', 'binnen', 'boven', 'bovenop', 'buiten', 'dichtbij']
surenouns = ['mama', 'papa']
longvowels = ['a', 'é', 'i', 'o', 'u', 'y']
vowels = ['a', 'e', 'i', 'o', 'u']


def makegen(lemma):
    if lemma is None or len(lemma) < 2:
        result = None
    elif lemma[-1] in ['s', 'z', 'x']:
        result = lemma + "'"
    elif lemma[-2:] in [ 'ij']:
        result = lemma + 's'
    elif lemma[-2] in vowels and lemma[-1] in vowels:
        result = lemma + 's'
    elif lemma[-1] in longvowels:
        result = lemma + "'s"
    else:
        result = lemma + 's'
    return result

def realword(node):
    result = True
    result = result and getattval(node, 'pt') not in ['tsw', 'let']
    result = result and getattval(node, 'lemma') not in ['xx', 'xxx', 'yyy', 'www', 'hè']
    result = result and getattval(node, 'lemma') not in filledpauseslexicon
    result = result or lemma(node) in surenouns


    return result


def hasgenitive(node):
    lemma = getattval(node, 'lemma')
    nodept = pt(node)
    if nodept not in ['n', 'vnw']:
        nodept = 'n'
    result = (lemma, nodept) in genlexicon and 'yes' in genlexicon[(lemma, nodept)]
    result = result or namepart_isa_namepart(lemma)
    return result

def aanwvnw(node):
    result = getattval(node, 'pt') == 'vnw' and getattval(node, 'vwtype') == 'aanw' and not rpronoun(node)
    return result


def n(node):
    result = getattval(node, 'pt') == 'n'
    return result


def getal(node):
    result = getattval(node, 'getal')
    return result

def pt(node):
    result = getattval(node, 'pt')
    return result

def bg(node):
    result = int(getattval(node, 'begin'))
    return result

def tw(node):
    result = getattval(node, 'pt') == 'tw'
    return result

def word(node):
    result = getattval(node, 'word')
    return result


def adj(node):
    result = getattval(node, 'pt') == 'adj'
    return result

def perspro(node):
    pt = getattval(node, 'pt')
    vwtype = getattval(node, 'vwtype')
    result = pt == 'vnw' and vwtype == 'pers'
    return result

def inf(node):
    result = getattval(node, 'pt') == 'ww' and getattval(node, 'wvorm') == 'inf'
    return result


def rpronoun(node):
    result = getattval(node, 'pt') == 'vnw' and \
             getattval(node, 'lemma') in ['er', 'hier', 'daar', 'ergens', 'overal', 'nergens', 'waar']
    return result

def bw(node):
    result = getattval(node, 'pt') == 'bw'
    return result

def ww(node):
    result = getattval(node, 'pt') == 'ww'
    return result


def lemma(node):
    result = getattval(node, 'lemma')
    return result

def predadv(node):
    result = locadv(node)
    result = result or (bw(node) and lemma(node) in ['niet', 'mee', 'weg'])
    return result

def vz(node):
    result = getattval(node, 'pt') == 'vz'
    return result

def locadv(node):
    result = getattval(node, 'pt') in ['bw', 'vz']
    frame = getattval(node, 'frame')
    result = result and ('loc' in frame or 'er_adverb' in frame)
    result = result or rpronoun(node)
    return result

def biglocvz(node):
    result = getattval(node, 'lemma') in biglocvzs
    return result

def getleavestr(leaves):
    leaveseq = ['{}:{}:{}:{}'.format(getattval(leave, 'end'), getattval(leave, 'word'), getattval(leave, 'lemma'),
                                     getattval(leave, 'pt')) for leave
                in leaves]
    leavestr = space.join(leaveseq)
    return leavestr

def knownnoun(node):
    word = getattval(node, 'word')
    lemma = getattval(node, 'lemma')
    postag = pt(node)
    result = postag == 'n' and (known_word(word) or known_word(lemma))
    result = result or lemma in surenouns
    return result

def nominal(node):
    result = pt(node) == 'n' or aanwvnw(node)
    return result

def mktoken(node, map):
    nodebegin = bg(node)
    nodeword = word(node)
    if nodebegin in map:
        nodepos = map[nodebegin]
    else:
        SDLOGGER.error('missing begin in map {}'.format(nodebegin))
        nodepos = int(nodebegin)
    result = Token(nodeword, nodepos)
    return result


def mktokenlist(leaves, themap, fpos, inserttokens):
    resultlist = [mktoken(lv, themap) for lv in leaves if bg(lv) <= fpos] + \
                 inserttokens + \
                 [mktoken(lv, themap) for lv in leaves if bg(lv) > fpos]
    return resultlist


def mkinsertmeta(inserttokens, resultlist):
    insertposs = [token.pos + token.subpos for token in inserttokens]
    insertwordlist = [token.word for token in inserttokens]
    tokenmappinglist = [token.pos if token.subpos == 0 else None for token in resultlist]
    metadata1 = [Meta(insertion, [insertword], annotatedposlist=[insertpos],
                 annotatedwordlist=[], annotationposlist=[insertpos],
                 annotationwordlist=[insertword], cat=smallclause, source=SASTA, penalty=defaultpenalty,
                 backplacement=bpl_delete) for insertword, insertpos in zip(insertwordlist, insertposs)]
    meta2 = Meta(insertiontokenmapping, tokenmappinglist, cat=tokenmapping, source=SASTA, penalty=0,
                 backplacement=bpl_none)
    metadata = metadata1 + [meta2]
    return metadata


def smallclauses(tokensmd, tree):
    resultlist = []
    leaves = getnodeyield(tree)
    reducedleaves = [leave for leave in leaves if realword(leave)]
    if not(len(reducedleaves) > 1 and len(reducedleaves) <= 3):
        return resultlist
    tokens = tokensmd.tokens
    treewords = [word(tokennode) for tokennode in leaves]
    tokenwords = [token.word for token in tokens if not token.skip]
    if treewords != tokenwords:
        SDLOGGER.error('Token mismatch: {} v. {}'.format(treewords, tokenwords))
        return []
    themap = {bg(tokennode): token.pos for (tokennode, token) in zip(leaves, tokens)}
    metadata = tokensmd.metadata

    if len(reducedleaves) <= 3:
        first = leaves[0]
        second = leaves[1]
    if len(reducedleaves) == 3:
        third = leaves[0]

    if len(reducedleaves) == 2:
        if (aanwvnw(first) or knownnoun(first) or perspro(first)) and (predadv(second)or vz(second) or bw(second)):
            fpos = int(getattval(first, 'begin'))
            inserttokens = [Token('moet' if getal(first) != 'mv' else 'moeten', fpos, subpos=5)]
            resultlist = mktokenlist(leaves, themap, fpos, inserttokens)
            metadata += mkinsertmeta(inserttokens, resultlist)
        elif (aanwvnw(second) or knownnoun(second) or perspro(second) or tw(second)) and predadv(first):
            fpos = int(getattval(first, 'begin'))
            inserttokens = [Token('moet' if getal(second) != 'mv' else 'moeten', fpos, subpos=5)]
            resultlist = mktokenlist(leaves, themap, fpos, inserttokens)
            metadata += mkinsertmeta(inserttokens, resultlist)
        elif (aanwvnw(first) or knownnoun(first)) and adj(second):
            fpos = int(getattval(first, 'begin'))
            inserttokens = [Token('is' if getal(first) != 'mv' else 'zijn', fpos, subpos=5)]
            resultlist = mktokenlist(leaves, themap, fpos, inserttokens)
            metadata += mkinsertmeta(inserttokens, resultlist)
        elif (aanwvnw(second) or knownnoun(second) or tw(second)) and biglocvz(first):
            fpos = int(getattval(first, 'begin'))
            inserttokens = [Token('is' if getal(first) != 'mv' else 'zijn', fpos, subpos=5)]
            resultlist = mktokenlist(leaves, themap, fpos, inserttokens)
        elif knownnoun(first) and knownnoun(second) and not(lemma(first) == lemma(second)):
            if hasgenitive(first):
                genform = makegen(lemma(first))
                fpos = int(getattval(first, 'begin'))
                inserttokens = [Token('[: ' + genform + ']', fpos, subpos=5)]
                resultlist = mktokenlist(leaves, themap, fpos, inserttokens)
                metadata += mkinsertmeta(inserttokens, resultlist)
            else:
                fpos = int(getattval(first, 'begin'))
                inserttokens = [Token('is' if getal(first) != 'mv' else 'zijn', fpos, subpos=5)]
                resultlist = mktokenlist(leaves, themap, fpos, inserttokens)
                metadata += mkinsertmeta(inserttokens, resultlist)
        elif (aanwvnw(first) or knownnoun(first)) and inf(second):
            if intransitive(second):
                firstsubject = True
            elif transitive(second) and ishuman(first):
                firstsubject = True
            elif pseudotr(second) and (ishuman(first) or isanimate(first)):
                firstsubject = True
            else:
                firstsubject = False
            if firstsubject:
                fpos = int(getattval(first, 'begin'))
                inserttokens = [Token('wil' if getal(first) != 'mv' else 'willen', fpos, subpos=5)]
            else:
                fpos = -1
                inserttokens = [Token('ik', fpos, subpos=5), Token('wil', fpos, subpos=8)]
            resultlist =  mktokenlist(leaves, themap, fpos, inserttokens)
            metadata += mkinsertmeta(inserttokens, resultlist)
        elif not nominal(first) and not ww(first) and inf(second):
            fpos = -1
            inserttokens = [Token('ik', fpos, subpos=5), Token('wil', fpos, subpos=8)]
            resultlist = mktokenlist(leaves, themap, fpos, inserttokens)
            metadata += mkinsertmeta(inserttokens, resultlist)
    if resultlist == []:
        result = []
    else:
        result = [TokenListMD(resultlist, metadata)]
    return result




