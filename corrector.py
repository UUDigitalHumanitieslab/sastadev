''''
Jij moet er dan voor zorgen dat je in de CHAT file die je produceert iedere uiting afgaat en een call doet naar een functie

getcorrection
met als argument de string van de uiting.

Deze functie geeft dan terug een tuple (correction, metadata)

waarbij
•	correction een string is die je op moet nemen in de chat file als de verbeterde uiting
•	metadata metadata zijn a la PaQu (type, name, value) o.a. origutt van type text met als waarde de inputstring

'''

import copy
import re

from alpino import getdehetwordinfo
from basicreplacements import (basicexpansions, basicreplacements,
                               getdisambiguationdict)
from cleanCHILDEStokens import cleantokens
from config import PARSE_FUNC, SDLOGGER
from dedup import (cleanwordofnort, find_duplicates2, find_janeenouduplicates,
                   find_simpleduplicates, find_substringduplicates2,
                   getfilledpauses, getprefixwords, getrepeatedtokens,
                   getunwantedtokens, nodesfindjaneenou)
from deregularise import correctinflection
from find_ngram import findmatches, ngram1
from iedims import getjeforms
from lexicon import de, dets, getwordinfo, het, informlexicon, known_word
from macros import expandmacros
# from alternative import Alternative, Replacement, Metadata, Meta
from metadata import (Meta, bpl_indeze, bpl_node, bpl_none, bpl_word,
                      bpl_wordlemma, defaultbackplacement, defaultpenalty,
                      filled_pause, fstoken, intj, janeenou, longrep,
                      mkSASTAMeta, repeated, repeatedjaneenou,
                      repeatedseqtoken, shortrep, substringrep, unknownsymbol)
from namepartlexicon import isa_namepart
from sastatok import sasta_tokenize
from sastatoken import Token, tokenlist2stringlist
from stringfunctions import (chatxxxcodes, consonants, deduplicate,
                             endsinschwa, fullworddehyphenate, monosyllabic,
                             vowels)
from sva import getsvacorrections
from tokenmd import TokenListMD, TokenMD, mdlist2listmd
from treebankfunctions import find1, getattval, getnodeyield

SASTA = 'SASTA'

repetition = 'Repetition'

replacepattern = '{} [: {} ]'
metatemplate = '##META {} {} = {}'
slash = '/'
space = ' '

disambiguationdict = getdisambiguationdict()

wrongdet_excluded_words = ['zijn', 'dicht', 'met', 'ik']


class Ngramcorrection:
    def __init__(self, ngram, fpositions, cpositions, metafunction):
        self.ngram = ngram
        self.fpositions = fpositions
        self.cpositions = cpositions
        self.metafunction = metafunction


def mkmeta(att, val, type='text'):
    result = metatemplate.format(type, att, val)
    return result


def anychars(chars):
    result = '[' + chars + ']'
    return result


def opt(pattern):
    result = '(' + pattern + ')?'
    return result


def replacement(inword, outword):
    result = replacepattern.format(inword, outword)
    return result


# duppattern = r'(.)\1{2,}'
# dupre = re.compile(duppattern)
gaatiepattern = r'^.*' + anychars(vowels) + opt(anychars(consonants)) + 'tie$'
gaatiere = re.compile(gaatiepattern)
neutersgnoun = 'boekje'  # seecet here an unambiguous neuter noun


def skiptokens(tokenlist, skiptokenlist):
    '''

    :param tokenlist:
    :param skiptokenlist:
    :return: a tokenlist identical to the input tokenlist but with the tokens that also occur with the same pos
    in skiptokenlist marked with skip=True
    '''
    skippositions = {token.pos for token in skiptokenlist}
    resultlist = []
    for token in tokenlist:
        if token.pos in skippositions:
            newtoken = Token(token.word, token.pos, skip=True)
        else:
            newtoken = token
        resultlist.append(newtoken)
    return resultlist


def ngramreduction(reducedtokens, token2nodemap, allremovetokens, allremovepositions, allmetadata, ngramcor):
    # metadat function should still be added / abstracted
    (fb, fe) = ngramcor.fpositions
    (cb, ce) = ngramcor.cpositions
    reducedleaves = [token2nodemap[tok.pos] for tok in reducedtokens]

    vnwpvvnwpvmatches = findmatches(ngramcor.ngram, reducedleaves)
    allfalsestarttokens = []
    metadata = []
    for match in vnwpvvnwpvmatches:
        positions = [pos for pos in range(match[0], match[1])]
        falsestartpositions = [tok.pos for i, tok in enumerate(reducedtokens) if i in positions[fb:fe]]
        falsestarttokens = [tok for tok in reducedtokens if tok.pos in falsestartpositions]
        allfalsestarttokens += falsestarttokens
        correcttokenpositions = [tok.pos for i, tok in enumerate(reducedtokens) if i in positions[cb:ce]]
        correcttokens = [tok for tok in reducedtokens if tok.pos in correcttokenpositions]
        allremovetokens += falsestarttokens
        allremovepositions += falsestartpositions
        metadata += ngramcor.metafunction(falsestarttokens, falsestartpositions, correcttokens)
    reducedtokens = [tok for tok in reducedtokens if tok not in allfalsestarttokens]
    allmetadata += metadata
    return reducedtokens, allremovetokens, allmetadata


def reduce(tokens, tree):

    if tree is None:
        SDLOGGER.error('No tree for :{}\nNo reduction applied'.format(tokens))
        return((tokens, []))

    tokennodes = tree.xpath('.//node[@pt or @pos]')
    tokennodesdict = {int(getattval(n, 'begin')): n for n in tokennodes}
    token2nodemap = {token.pos: tokennodesdict[token.pos] for token in tokens if keycheck(token.pos, tokennodesdict)}

    reducedtokens = tokens
    allmetadata = []

    allremovetokens = []
    allremovepositions = []

    # throw out unwanted symbols - -- # etc
    unwantedtokens = getunwantedtokens(reducedtokens)
    unwantedpositions = [tok.pos for tok in unwantedtokens]
    allremovetokens += unwantedtokens
    allremovepositions += unwantedpositions
    reducedtokens = [n for n in reducedtokens if n not in unwantedtokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', unknownsymbol, 'Syntax') for token in unwantedtokens]
    allmetadata += metadata

    # remove  filled pauses

    filledpausetokens = getfilledpauses(reducedtokens)
    filledpausepositions = [token.pos for token in filledpausetokens]
    allremovetokens += filledpausetokens
    allremovepositions += filledpausepositions
    reducedtokens = [tok for tok in reducedtokens if tok not in filledpausetokens]
    reducednodes = [token2nodemap[tok.pos] for tok in reducedtokens if keycheck(tok.pos, token2nodemap)]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', filled_pause, 'Syntax') for token in filledpausetokens]
    allmetadata += metadata

    # remove tsw incl goh och hé oke but not ja, nee, nou
    tswtokens = [n for n in reducedtokens if n.pos in token2nodemap
                 and getattval(token2nodemap[n.pos], 'pt') == 'tsw'
                 and getattval(token2nodemap[n.pos], 'lemma') not in {'ja', 'nee', 'nou'}]
    tswpositions = [n.pos for n in tswtokens]
    allremovetokens += tswtokens
    allremovepositions == tswpositions
    reducedtokens = [n for n in reducedtokens if n not in tswtokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', intj, 'Syntax') for token in tswtokens]
    allmetadata += metadata

    # find duplicatenode repetitions of ja, nee, nou
    janeenouduplicatenodes = find_janeenouduplicates(reducedtokens)
    allremovetokens += janeenouduplicatenodes
    reducedtokens = [n for n in reducedtokens if n not in janeenouduplicatenodes]
    reducednodes = [token2nodemap[tok.pos] for tok in reducedtokens if keycheck(tok.pos, token2nodemap)]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', repeatedjaneenou, 'Syntax', subcat=repetition)
                for token in janeenouduplicatenodes]
    allmetadata += metadata

    # ASTA sec 6.3 p. 11
    # remove ja nee nou

    janeenounodes = nodesfindjaneenou(reducednodes)
    janeenoutokens = [tok for tok in reducedtokens if keycheck(tok.pos, token2nodemap) and token2nodemap[tok.pos] in janeenounodes]
    janeenoupositions = [token.pos for token in janeenoutokens]
    allremovetokens += janeenoutokens
    allremovepositions += janeenoupositions
    reducedtokens = [tok for tok in reducedtokens if tok not in janeenoutokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', janeenou, 'Syntax') for token in janeenoutokens]
    allmetadata += metadata

    # short repetitions
    def oldcond(x, y): return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) < .5 and not informlexicon(cleanwordofnort(x))
    def cond(x, y): return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) < .5  # check on lexicon put off actually two variants should be tried if the word is an existin gword
    shortprefixtokens = getprefixwords(reducedtokens, cond)
    shortprefixpositions = [token.pos for token in shortprefixtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, shortprefixtokens)
    allremovetokens += shortprefixtokens
    allremovepositions += shortprefixpositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', shortrep, 'Tokenisation', subcat=repetition) for token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in shortprefixtokens]

    # long repetitions
    def cond(x, y): return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) >= .5 and not informlexicon(cleanwordofnort(x))
    longprefixtokens = getprefixwords(reducedtokens, cond)
    longprefixpositions = [token.pos for token in longprefixtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, longprefixtokens)
    allremovetokens += longprefixtokens
    allremovepositions += longprefixpositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', longrep, 'Tokenisation', subcat=repetition) for token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in longprefixtokens]

    # find unknown words that are a substring of their successor
    substringtokens, _ = find_substringduplicates2(reducedtokens)
    substringpositions = [token.pos for token in substringtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, substringtokens)
    allremovetokens += substringtokens
    allremovepositions += substringpositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', substringrep, 'Tokenisation',
                            subcat=repetition) for token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in substringtokens]

    # simple duplicates
    dupnodetokens = find_simpleduplicates(reducedtokens)
    dupnodepositions = [token.pos for token in dupnodetokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, dupnodetokens)
    allremovetokens += dupnodetokens
    allremovepositions += dupnodepositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical',
                            repeated, 'Tokenisation', subcat=repetition) for token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in dupnodetokens]

    # duplicate sequences
    dupnodetokens, dupinfo = find_duplicates2(reducedtokens)
    dupnodepositions = [token.pos for token in dupnodetokens]
    duppairs = []
    for token in dupnodetokens:
        for othertok in reducedtokens:
            if token.pos in dupinfo.longdups and othertok.pos == dupinfo.longdups[token.pos]:
                nwt = othertok
                duppairs.append((token, nwt))
                break
    allremovetokens += dupnodetokens
    allremovepositions += dupnodepositions
    metadata = [mkSASTAMeta(token, nwt, 'ExtraGrammatical',
                            repeatedseqtoken, 'Tokenisation', subcat=repetition)
                for token, nwt in duppairs]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in dupnodetokens]

    # remove unknown words if open class DO NOT DO this
    # unknown_word_tokens = [tok for tok in reducedtokens if getattval(token2nodemap[tok.pos], 'pt') in openclasspts
    #                        and not (asta_recognised_wordnode(token2nodemap[tok.pos]))]
    # unknown_word_positions = [token.pos for token in unknown_word_tokens]
    # allremovetokens += unknown_word_tokens
    # allremovepositions += unknown_word_positions
    # metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical',
    #                         unknownword, 'Tokenisation')
    #             for token in reducedtokens if token in unknown_word_tokens]
    # allmetadata += metadata
    # reducedtokens = [n for n in reducedtokens if n not in unknown_word_tokens]

    # ngram based cases

    # vnw pv vnw pv

    def metaf(falsestarttokens, falsestartpositions, correcttokens): return \
        [Meta('Retracing', 'Retracing with Correction', annotatedposlist=falsestartpositions,
              annotatedwordlist=[c.word for c in falsestarttokens],
              annotationposlist=[c.pos for c in correcttokens],
              annotationwordlist=[c.word for c in correcttokens], cat='Retracing', subcat=None, source=SASTA,
              penalty=defaultpenalty, backplacement=bpl_none)] + \
        [mkSASTAMeta(ftoken, ctoken, 'Retracing with Correction', fstoken, 'Retracing')
         for ftoken, ctoken in zip(falsestarttokens, correcttokens)]

    vnwpvvnwpvcor = Ngramcorrection(ngram1, (0, 2), (2, 4), metaf)
    reducedtokens, allremovetokens, allmetadata = ngramreduction(reducedtokens, token2nodemap, allremovetokens,
                                                                 allremovepositions, allmetadata, vnwpvvnwpvcor)

    # reducedleaves = [token2nodemap[tok.pos] for tok in reducedtokens]
    #
    # vnwpvvnwpvmatches = findmatches(ngram1, reducedleaves)
    # allfalsestarttokens = []
    # metadata = []
    # for match in vnwpvvnwpvmatches:
    #     positions = [pos for pos in range(match[0], match[1])]
    #     falsestartpositions = [tok.pos for i, tok in enumerate(reducedtokens) if i in positions[0:2]]
    #     falsestarttokens = [tok for tok in reducedtokens if tok.pos in falsestartpositions]
    #     allfalsestarttokens += falsestarttokens
    #     correcttokenpositions = [tok.pos for i, tok in enumerate(reducedtokens) if i in positions[2:5]]
    #     correcttokens = [tok for tok in reducedtokens if tok.pos in correcttokenpositions]
    #     allremovetokens += falsestarttokens
    #     allremovepositions += falsestartpositions
    #     metadata += [Meta('Retracing', 'Retracing with Correction',  annotatedposlist=falsestartpositions,
    #                  annotatedwordlist=[c.word for c in falsestarttokens], annotationposlist=[c.pos for c in correcttokens],
    #                  annotationwordlist=[c.word for c in correcttokens], cat='Retracing', subcat=None, source=SASTA,
    #                     penalty=defaultpenalty, backplacement=bpl_none)]
    #     metadata += [mkSASTAMeta(ftoken, ctoken, 'Retracing with Correction', fstoken,  'Retracing', )
    #                 for ftoken, ctoken  in zip(falsestarttokens, correcttokens)]
    #
    # reducedtokens = [tok for tok in reducedtokens if tok not in allfalsestarttokens]
    # allmetadata += metadata

    skipmarkedtokens = skiptokens(tokens, allremovetokens)

    # return (reducedtokens, allremovetokens, allmetadata)
    return (skipmarkedtokens, allmetadata)


def keycheck(key, dict):
    if key not in dict:
        SDLOGGER.error('key {}  not in dictionary. Contents of dictionary:'.format(key))
        for akey, val in dict.items():
            valbgn = getattval(val, 'begin')
            valpt = getattval(val, 'pt')
            valword = getattval(val, 'word')
            valstr = '{}:{}:{}'.format(valbgn, valpt, valword)
            SDLOGGER.error('{}={}'.format(akey, valstr))
    return key in dict


def combinesorted(toklist1, toklist2):
    result = toklist1 + toklist2
    sortedresult = sorted(result, key=lambda tok: tok.pos)
    return sortedresult


def getcorrection(utt, tree=None, interactive=False):
    # NOT used anymore!!!!

    allmetadata = []
    rawtokens = sasta_tokenize(utt)
    wordlist = tokenlist2stringlist(rawtokens)

    tokens, metadata = cleantokens(rawtokens, repkeep=False)
    allmetadata += metadata
    tokensmd = TokenListMD(tokens, [])

    # reducedtokens, allremovedtokens, metadata = reduce(tokens)
    # allremovedtokens, metadata = reduce(tokens)
    skipmarkedtokens, metadata = reduce(tokens, tree)
    # reducedtokensmd = TokenListMD(reducedtokens, [])
    reducedtokensmd = TokenListMD(skipmarkedtokens, [])

    alternativemds = getalternatives(reducedtokensmd, tree, 0)
    # alternativemds = getalternatives(tokensmd, allremovedtokens, tree, 0)
    # unreducedalternativesmd = [TokenListMD(combinesorted(alternativemd.tokens, allremovedtokens), alternativemd.metadata) for alternativemd in alternativemds]

    # correctiontokensmd = unreducedalternativesmd[-1] if unreducedalternativesmd != [] else tokensmd
    correctiontokensmd = alternativemds[-1] if alternativemds != [] else tokensmd

    correction = tokenlist2stringlist(correctiontokensmd.tokens)
    allmetadata += correctiontokensmd.metadata

    result = (correction, allmetadata)
    return result


def getcorrections(utt, method, tree=None, interactive=False):

    origutt = utt
    allmetadata = []
    rawtokens = sasta_tokenize(utt)
    wordlist = tokenlist2stringlist(rawtokens)

    # check whether the tree has the same yield
    origtree = tree
    treeyield = getnodeyield(tree)
    treewordlist = [getattval(n, 'word') for n in treeyield]

    if treewordlist != wordlist:
        revisedutt = space.join(wordlist)
        tree = PARSE_FUNC(revisedutt)

    tokens, metadata = cleantokens(rawtokens, repkeep=False)
    allmetadata += metadata
    tokensmd = TokenListMD(tokens, [])

    # reducedtokens, allremovedtokens, metadata = reduce(tokens)
    reducedtokens, metadata = reduce(tokens, tree)
    reducedtokensmd = TokenListMD(reducedtokens, [])
    allmetadata += metadata

    # alternativemds = getalternatives(reducedtokensmd, tree, 0)
    alternativemds = getalternatives(reducedtokensmd, method, tree, 0)
    # unreducedalternativesmd = [TokenListMD(combinesorted(alternativemd.tokens, allremovedtokens), alternativemd.metadata) for alternativemd in alternativemds]

    intermediateresults = alternativemds if alternativemds != [] else [tokensmd]

    results = []
    for ctmd in intermediateresults:
        # correction = tokenlist2stringlist(ctmd.tokens)
        correction = ctmd.tokens
        themetadata = allmetadata + ctmd.metadata
        results.append((correction, themetadata))
    return results


# def getalternatives(origtokensmd, method, llremovedtokens, tree, uttid):
def getalternatives(origtokensmd, method, tree, uttid):

    tokensmd = explanationasreplacement(origtokensmd, tree)
    if tokensmd is None:
        tokensmd = origtokensmd

    tokens = tokensmd.tokens
    allmetadata = tokensmd.metadata
    newtokens = []
    alternatives = []
    alternativetokenmds = {}
    validalternativetokenmds = {}
    tokenctr = 0
    for token in tokens:
        tokenmd = TokenMD(token, allmetadata)
        alternativetokenmds[tokenctr] = getalternativetokenmds(tokenmd, method, tokens, tokenctr, tree, uttid)
        validalternativetokenmds[tokenctr] = getvalidalternativetokenmds(tokenmd, alternativetokenmds[tokenctr])
        tokenctr += 1

    # get all the new token sequences
    tokenctr = 0
    lvalidalternativetokenmds = len(validalternativetokenmds)
    altutts = [[]]
    newutts = []
    while tokenctr < lvalidalternativetokenmds:
        for tokenmd in validalternativetokenmds[tokenctr]:
            for utt in altutts:
                newutt = copy.copy(utt)
                newutt.append(tokenmd)
                newutts.append(newutt)
        altutts = newutts
        newutts = []
        tokenctr += 1

    # now turn each sequence of (token, md) pairs into a pair (tokenlist, mergedmetadata)
    newaltuttmds = []
    for altuttmd in altutts:
        newaltuttmd = mdlist2listmd(altuttmd)
        newaltuttmds.append(newaltuttmd)

    # basic expansions

    allalternativemds = newaltuttmds

    newresults = []
    for uttmd in allalternativemds:
        expansionmds = getexpansions(uttmd)
        newresults += expansionmds
    allalternativemds += newresults

    # combinations of tokens or their alternatives: de kopje, de stukkie, heeft gevalt

    newresults = []
    for uttmd in allalternativemds:
        # utterance = space.join([token.word for token in uttmd.tokens])
        utterance, _ = mkuttwithskips(uttmd.tokens)
        ntree = PARSE_FUNC(utterance)
        newresults += getwrongdetalternatives(uttmd, ntree, uttid)
    allalternativemds += newresults

    newresults = []
    for uttmd in allalternativemds:
        # utterance = space.join([token.word for token in uttmd.tokens])
        utterance, _ = mkuttwithskips(uttmd.tokens)
        # reducedtokens = [t for t in uttmd.tokens if not t.skip]
        # reduceduttmd = TokenListMD(reducedtokens, uttmd.metadata)
        ntree = PARSE_FUNC(utterance)
        # simpleshow(ntree)
        uttalternativemds = getsvacorrections(uttmd, ntree, uttid)
        newresults += uttalternativemds
    allalternativemds += newresults

    newresults = []
    for uttmd in allalternativemds:
        # utterance = space.join([token.word for token in uttmd.tokens])
        utterance, _ = mkuttwithskips(uttmd.tokens)
        ntree = PARSE_FUNC(utterance)
        newresults += correctPdit(uttmd, ntree, uttid)
    allalternativemds += newresults

    # final check whether the alternatives are improvements. It is not assumed that the original tokens is included in the alternatives
    finalalternativemds = lexcheck(tokensmd, allalternativemds)

    return finalalternativemds


skiptemplate = "[ @skip {} ]"


def oldmkuttwithskips(tokens, toskip):
    sortedtokens = sorted(tokens, key=lambda x: x.pos)
    resultlist = []
    for token in sortedtokens:
        if token in toskip:
            resultlist.append(skiptemplate.format(token.word))
        else:
            resultlist.append(token.word)
    result = space.join(resultlist)
    return result


def mkuttwithskips(tokens, delete=True):
    sortedtokens = sorted(tokens, key=lambda x: x.pos)
    resultlist = []
    tokenposlist = []
    for token in sortedtokens:
        if token.skip:
            if not delete:
                resultlist.append(skiptemplate.format(token.word))
                tokenposlist.append(token.pos)
        else:
            resultlist.append(token.word)
            tokenposlist.append(token.pos)
    result = space.join(resultlist)

    return result, tokenposlist


def getexpansions(uttmd):
    expansionfound = False
    newtokens = []
    tokenctr = 0
    newtokenctr = 0
    tokenposlist = []
    newmd = uttmd.metadata
    for token in uttmd.tokens:
        if token.word.lower() in basicexpansions:
            expansionfound = True
            for (rlist, c, n, v) in basicexpansions[token.word.lower()]:
                for rw in rlist:
                    newtoken = Token(rw, newtokenctr)
                    newtokens.append(newtoken)
                    tokenposlist.append(token.pos)
                    newtokenctr += 1
                    nwt = Token(space.join(rlist), token.pos)
                meta1 = mkSASTAMeta(token, nwt, n, v, c, subcat=None, penalty=defaultpenalty,
                                    backplacement=bpl_none)
                newmd.append(meta1)

        else:
            newtoken = Token(token.word, newtokenctr)
            newtokens.append(newtoken)
            tokenposlist.append(token.pos)
            tokenctr += 1
            newtokenctr += 1

    # adapt the metadata
    if expansionfound:
        meta2 = Meta('OrigCleanTokenPosList', tokenposlist, annotatedposlist=[],
                     annotatedwordlist=[], annotationposlist=tokenposlist,
                     annotationwordlist=[], cat='Tokenisation', subcat=None, source=SASTA, penalty=defaultpenalty,
                     backplacement=bpl_none)
        newmd.append(meta2)
        result = [TokenListMD(newtokens, newmd)]
    else:
        result = []

    return result


def lexcheck(intokensmd, allalternativemds):
    finalalternativemds = [intokensmd]
    for alternativemd in allalternativemds:
        diff_found = False
        include = True
        intokens = intokensmd.tokens
        outtokens = alternativemd.tokens
        if len(intokens) != len(outtokens):
            diff_found = True
        else:
            for (intoken, outtoken) in zip(intokens, outtokens):
                if intoken != outtoken:
                    diff_found = True
                    if not known_word(outtoken.word):
                        include = False
                        break
        if diff_found and include:
            finalalternativemds.append(alternativemd)
    return finalalternativemds

# moved to metadata
# def mkSASTAMeta(token, nwt, name, value, cat, subcat=None, penalty=defaultpenalty, backplacement=defaultbackplacement):
#    result = Meta(name, value, annotatedposlist=[token.pos],
#                     annotatedwordlist=[token.word], annotationposlist=[nwt.pos],
#                     annotationwordlist=[nwt.word], cat=cat, subcat=subcat, source=SASTA, penalty=penalty,
#                     backplacement=backplacement)
#    return result


def updatenewtokenmds(newtokenmds, token, newwords, beginmetadata, name, value, cat, subcat=None,
                      penalty=defaultpenalty, backplacement=defaultbackplacement):
    for nw in newwords:
        nwt = Token(nw, token.pos)
        meta = mkSASTAMeta(token, nwt, name=name, value=value, cat=cat, subcat=subcat, penalty=penalty,
                           backplacement=backplacement)
        metadata = [meta] + beginmetadata
        newwordtokenmd = TokenMD(nwt, metadata)
        newtokenmds.append(newwordtokenmd)
    return newtokenmds


def gettokensplusxmeta(tree):
    '''
    converts the origutt into  list of xmeta elements
    :param tree: input tree
    :return: list of xmeta elements
    '''
    origutt = find1(tree, './/meta[@name="origutt"]/@value')
    tokens1 = sasta_tokenize(origutt)
    tokens2, metadata = cleantokens(tokens1, repkeep=False)
    return tokens2, metadata


def findxmetaatt(xmetalist, name, cond=lambda x: True):
    cands = [xm for xm in xmetalist if xm.name == name and cond(xm)]
    if cands == []:
        result = None
    else:
        result = cands[0]
    return result


def tokenreplace(oldtokens, newtoken):
    newtokens = []
    for token in oldtokens:
        if token.pos == newtoken.pos:
            newtokens.append(newtoken)
        else:
            newtokens.append(token)
    return newtokens


def explanationasreplacement(tokensmd, tree):
    # interpret single word explanation as replacement # this will work only after retokenistion of the origutt
    result = None
    origmetadata = tokensmd.metadata
    xtokens, xmetalist = gettokensplusxmeta(tree)
    explanations = [xm for xm in xmetalist if xm.name == 'Explanation']
    newtokens = copy.deepcopy(xtokens)
    newmetadata = origmetadata + xmetalist
    for explanation in explanations:
        newwordlist = explanation.annotationwordlist
        oldwordlist = explanation.annotatedwordlist
        tokenposlist = explanation.annotatedposlist
        if len(newwordlist) == 1 and len(tokenposlist) == 1 and len(oldwordlist) == 1:
            newword = newwordlist[0]
            oldwordpos = tokenposlist[0]
            oldword = oldwordlist[0]
            newtoken = Token(newword, oldwordpos)
            oldtoken = Token(oldword, oldwordpos)
            if known_word(newword):
                newtokens = tokenreplace(newtokens, newtoken)
                bpl = bpl_node if known_word(oldword) else bpl_word
                meta = mkSASTAMeta(oldtoken, newtoken, name='ExplanationasReplacement', value='ExplanationasReplacement',
                                   cat='Lexical Error', backplacement=bpl_node)
                newmetadata.append(meta)
                result = TokenListMD(newtokens, newmetadata)
    return result


# some words are known but very unlikely as such
specialdevoicingwords = {'fan'}


def initdevoicing(token, voiceless, voiced, newtokenmds, beginmetadata):

    # initial s -> z, f -> v
    if not known_word(token.word.lower()) or token.word.lower() in specialdevoicingwords:
        if token.word[0] == voiceless:
            newword = voiced + token.word[1:]
            if known_word(newword):
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Pronunciation Variant', value='Initial {} devoicing'.format(voiced),
                                                cat='Pronunciation', backplacement=bpl_word)

    return newtokenmds


def getalternativetokenmds(tokenmd, method, tokens, tokenctr, tree, uttid):

    token = tokenmd.token
    beginmetadata = tokenmd.metadata
    newtokenmds = []

    if token.skip:
        return newtokenmds

    # decapitalize initial token  except when it is a known name
    if tokenctr == 0 and token.word.istitle() and not isa_namepart(token.word):
        newword = token.word.lower()

        newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                        name='Character Case', value='Lower case', cat='Orthography')

    # dehyphenate
    if not known_word(token.word):
        newwords = fullworddehyphenate(token.word, known_word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Dehyphenation', value='Dehyphenation', cat='Pronunciation',
                                        backplacement=bpl_word)

    # deduplicate jaaaaa -> ja; heeeeeel -> heel
    if not known_word(token.word):
        newwords = deduplicate(token.word, known_word, exceptions=chatxxxcodes)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Emphasis', value='Phoneme lengthening', cat='Pronunciation',
                                        backplacement=bpl_word)

    # basic replacements replace as by als, isse by is
    # here come the replacements
    if token.word.lower() in basicreplacements:
        for (r, c, n, v) in basicreplacements[token.word.lower()]:
            newwords = [r]
            newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                            name=n, value=v, cat=c, backplacement=bpl_word)

    moemoetxpath = './/node[@lemma="moe" and @pt!="n" and not(%onlywordinutt%) and (@rel="--" or @rel="dp" or @rel="predm" or @rel="nucl")]'
    expanded_moemoetxpath = expandmacros(moemoetxpath)
    if token.word.lower() == 'moe' and tree.xpath(expanded_moemoetxpath) != []:
        newwords = ['moet']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Informal pronunciation', value='Final t-deletion', cat='Pronunciation',
                                        backplacement=bpl_word)

    # dee -> deze of deed
    if token.word.lower() == 'dee':
        newwords = ['deze']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Wrong pronunciation', value='Coda reduction', cat='Pronunciation',
                                        backplacement=bpl_word, penalty=5)
        newwords = ['deed']
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Informal pronunciation', value='Final t-deletion', cat='Pronunciation',
                                        backplacement=bpl_word)

    # find document specific replacements

    # find organisation specific replacements

    # find childes replacements, preferably with vocabulary from the same age

    # gaatie
    if not known_word(token.word):
        newwords = gaatie(token.word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Word combination', value='Cliticisation', cat='Pronunciation',
                                        backplacement=bpl_none)

    # extend to gaat-ie

    # dediacritisize

    # iedims
    if token.word.endswith('ie') or token.word.endswith('ies'):
        newwords = getjeforms(token.word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='RegionalForm', value='ieDim', cat='Morphology', backplacement=bpl_word)

    # overregularised verb forms: gevalt -> gevallen including  incl  wrong verb forms: gekeekt -> gekeken
    if not known_word(token.word):
        nwms = correctinflection(token.word)
        for nw, metavalue in nwms:
            newtokenmds += updatenewtokenmds(newtokenmds, token, [nw], beginmetadata,
                                             name='InflectionError', value=metavalue, cat='Morphology',
                                             backplacement=bpl_word)

    # wrong verb forms: gekeekt -> gekeken: done!

    # me ze (grote/oudere/ kleine) moeder /vader/zusje/ broer -> mijn me s done by Alpiono, here we do ze
    # next xpath does not work becasue it must be preceded by a . !!
    # zexpathmodel = """//node[@word="ze" and @begin={begin} and (@rel="--"  or (@rel="obj1" and parent::node[@cat="pp"])) and @end = ancestor::node[@cat="top"]/descendant::node[@pt="n"]/@begin]"""
    if token.word.lower() == 'ze' or token.word.lower() == 'su':
        # find the node that corresponds to this token in the tree
        # zexpath = zexpathmodel.format(begin=str(tokenctr))
        # zenode = find1(tree, zexpath)
        tokennodes = getnodeyield(tree)
        zenode = tokennodes[tokenctr]
        nexttoken = tokens[tokenctr + 1]  # do not take it from the tree because it may have been replaced by something else, e.g. avoid: ze dee -> ze deed -/-> z'n deed!
        zerel = getattval(zenode, 'rel')
        zeparent = zenode.getparent()
        zeparentcat = getattval(zeparent, 'cat')
        # nextpt = getattval(nextnode, 'pt')
        nexttokeninfo = getwordinfo(nexttoken.word.lower())
        nexttokenpts = {pt for (pt, _, _, _) in nexttokeninfo}
        if (zerel == '--' or zerel == 'mwp' or (zerel == 'obj1' and zeparentcat == 'pp')) and 'n' in nexttokenpts:
            newword = "z'n"
            newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                            name='Pronunciation Variant', value='N-less informal possessive pronoun',
                                            cat='Pronunciation', backplacement=bpl_word)

    # e-> e(n)
    enexceptions = {'inne'}
    if not known_word(token.word) and token.word.lower() not in basicreplacements and token.word.lower() not in enexceptions:
        if endsinschwa(token.word) and not monosyllabic(token.word):
            newword = token.word + 'n'
            if known_word(newword):
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Pronunciation Variant', value='N-drop after schwa',
                                                cat='Pronunciation', backplacement=bpl_word)

    # initial s -> z
    newtokenmds = initdevoicing(token, 's', 'z', newtokenmds, beginmetadata)
    # initial f -> v
    newtokenmds = initdevoicing(token, 'f', 'v', newtokenmds, beginmetadata)

    # replaceambiguous words with one reading not known by the child by a nonambiguous word with the same properties
    if method in {'tarsp', 'stap'}:
        if token.word.lower() in disambiguationdict:
            newword = disambiguationdict[token.word.lower()]
            newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                            name='Disambiguation', value='Avoid unknown reading',
                                            cat='Lexicon', backplacement=bpl_wordlemma)

    # ...en -> e: groten  -> grote (if adjective); goten -> grote

    # drop e at the end incl duplicated consonants (ooke -> ook; isse -> is ? DOne, basicreplacements

    # losse e -> een / het / de

    for newtokenmd in newtokenmds:
        morenewtokenmds = getalternativetokenmds(newtokenmd, method, tokens, tokenctr, tree, uttid)
        newtokenmds += morenewtokenmds

    return newtokenmds


def getvalidalternativetokenmds(tokenmd, newtokenmds):

    validnewtokenmds = [tokenmd for tokenmd in newtokenmds if known_word(tokenmd.token.word)]
    if validnewtokenmds == []:
        validnewtokenmds = [tokenmd]
    return validnewtokenmds


def gaatie(word):
    results = []
    if gaatiere.match(word):
        if informlexicon(word[:-2]):  # and if it is a verb this is essential because now tie is also split into t ie
            result = space.join([word[:-2], word[-2:]])
            results.append(result)
    return results


def getwrongdetalternatives(tokensmd, tree, uttid):
    correctiondone = False
    tokens = tokensmd.tokens
    metadata = tokensmd.metadata
    ltokens = len(tokens)
    tokenctr = 0
    newtokens = []
    while tokenctr < ltokens:
        token = tokens[tokenctr]
        if not token.skip and token.word in dets[de] and tokenctr < ltokens - 1:
            nexttoken = tokens[tokenctr + 1]
            # we want to exclude some words
            if nexttoken.skip:
                wordinfos = []
            elif nexttoken.word in wrongdet_excluded_words:
                wordinfos = []
            else:
                wordinfos, _ = getdehetwordinfo(nexttoken.word)
            if wordinfos != []:
                for wordinfo in wordinfos:  # if there are multiple alternatives we overwrite and therefore get the last alternative
                    (pos, dehet, infl, lemma) = wordinfo
                    if dehet == het and infl in ['e', 'de']:
                        # newcurtoken = replacement(token, swapdehet(token))
                        newcurtokenword = swapdehet(token.word)
                        newcurtoken = Token(newcurtokenword, token.pos)
                        meta = mkSASTAMeta(token, newcurtoken, name='GrammarError', value='deheterror', cat='Error',
                                           backplacement=bpl_node)
                        metadata.append(meta)
                    else:
                        newcurtokenword = token.word
                newtokens.append(Token(newcurtokenword, token.pos))
                correctiondone = True
            else:
                newcurtokenword = token.word
                newtokens.append(token)
        else:
            newtokens.append(token)
        tokenctr += 1
    result = TokenListMD(newtokens, metadata)
    if correctiondone:
        results = [result]
    else:
        results = []
    return results


def getindezemwp(prevtokennode, tokennode):
    ok = True
    ok = ok and getattval(prevtokennode, 'lemma') in {'in'}
    ok = ok and getattval(prevtokennode, 'rel') in {'mwp'}
    ok = ok and getattval(tokennode, 'lemma') in {'deze'}
    ok = ok and getattval(tokennode, 'rel') in {'mwp'}
    return ok


def correctPdit(tokensmd, tree, uttid):
    correctiondone = False
    tokennodes = getnodeyield(tree)
    tokens = tokensmd.tokens
    metadata = tokensmd.metadata
    newtokens = []
    tokenctr = 0
    prevtoken = None
    for token in tokens:
        tokennode = next(filter(lambda x: getattval(x, 'begin') == str(tokenctr), tokennodes), None)
        tokenlemma = getattval(tokennode, 'lemma')
        if not token.skip and prevtoken is not None and not prevtoken.skip and tokenlemma in {'dit', 'dat', 'deze', 'die'}:
            tokenrel = getattval(tokennode, 'rel')
            tokenpt = getattval(tokennode, 'pt')
            prevtokennode = tokennodes[tokenctr - 1] if tokenctr > 0 else None
            if prevtokennode is not None:
                prevpt = getattval(prevtokennode, 'pt')
                prevparent = prevtokennode.getparent()
                prevparentrel, prevparentcat = getattval(prevparent, 'rel'), getattval(prevparent, 'cat')
                indezemwp = getindezemwp(prevtokennode, tokennode)
                if (prevpt == 'vz' and prevparentcat != 'pp' and tokenrel not in {'obj1', 'det'} and tokenpt == 'vnw') or \
                        indezemwp:
                    newtoken = Token('hem', tokenctr)
                    bpl = bpl_indeze if indezemwp else bpl_node
                    meta = mkSASTAMeta(token, newtoken, name='parsed as', value='hem', cat='AlpinoImprovement',
                                       backplacement=bpl)
                    metadata.append(meta)
                    newtokens.append(newtoken)
                    correctiondone = True
                else:
                    newtokens.append(token)
            else:
                newtokens.append(token)
        else:
            newtokens.append(token)
        tokenctr += 1
        prevtoken = token
    result = TokenListMD(newtokens, metadata)
    if correctiondone:
        results = [result]
    else:
        results = []
    return results


def parseas(w, code):
    result = '[ @add_lex {} {} ]'.format(code, w)
    return result


def swapdehet(dedet):
    if dedet in dets[de]:
        deindex = dets[de].index(dedet)
    else:
        deindex = -1
    if dedet in dets[het]:
        hetindex = dets[het].index(dedet)
    else:
        hetindex = -1
    if deindex >= 0:
        result = dets[het][deindex]
    elif hetindex >= 0:
        result = dets[de][hetindex]
    else:
        result = None
    return result


def outputalternatives(tokens, alternatives, outfile):
    for el in alternatives:
        print(tokens[el], slash.join(alternatives[el]), file=outfile)


def mkchatutt(intokens, outtokens):
    result = []
    for (intoken, outtoken) in zip(intokens, outtokens):
        newtoken = intoken if intoken == outtoken else replacement(intoken, outtoken)
        result.append(newtoken)
    return result


def altmkchatutt(intokens, outtoken):
    result = []
    for intoken in intokens:
        newtoken = intoken if intoken == outtoken else replacement(intoken, outtoken)
        result.append(newtoken)
    return result
