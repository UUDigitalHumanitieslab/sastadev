from collections import defaultdict
from copy import copy, deepcopy

from lxml import etree

from basicreplacements import basicreplacements
from cleanCHILDEStokens import cleantext
from corrector import getcorrections, mkuttwithskips
from lexicon import de, dets, known_word
from metadata import (Meta, bpl_delete, bpl_indeze, bpl_node, bpl_none,
                      bpl_word, bpl_wordlemma)
from sastatok import sasta_tokenize
from sastatoken import tokenlist2stringlist
from sva import phicompatible
from targets import get_mustbedone
from treebankfunctions import (adaptsentence, add_metadata, countav,
                               deletewordnodes, find1, getattval, getbeginend,
                               getcompoundcount, getnodeyield, getsentid,
                               gettokposlist, getyield, myfind, showflatxml,
                               simpleshow, transplant_node, showtree)
from config import PARSE_FUNC, SDLOGGER
from metadata import insertion

ampersand = '&'

corr0, corr1, corrn = '0', '1', 'n'
validcorroptions = [corr0, corr1, corrn]

space = ' '
origuttxpath = './/meta[@name="origutt"]/@value'
uttidxpath = './/meta[@name="uttid"]/@value'
metadataxpath = './/metadata'
dezeAVntemplate = '<node begin="{begin}" buiging="met-e" end="{end}" frame="determiner(de,nwh,nmod,pro,nparg)" ' \
                  'id="{id}" infl="de" lcat="np" lemma="deze" naamval="stan" npagr="rest" pdtype="det" pos="det" ' \
                  'positie="nom" postag="VNW(aanw,det,stan,nom,met-e,rest)" pt="vnw" rel="obj1" root="deze" ' \
                  'sense="deze" vwtype="aanw" wh="nwh" word="deze"/>'

contextualproperties = ['rel', 'index', 'positie']

errorwbheader = ['Sample', 'User1', 'User2', 'User3'] + \
                ['Status', 'Uttid', 'Origutt', 'Origsent'] + \
                ['altid', 'altsent', 'score', 'penalty', 'dpcount', 'dhyphencount', 'dimcount', 'compcount', 'supcount',
                 'compoundcount', 'unknownwordcount', 'sucount', 'svaokcount', 'deplusneutcount', 'goodcatcount',
                 'hyphencount', 'basicreplaceecount']


def get_origandparsedas(metadatalist):
    parsed_as = None
    origutt = None
    for meta in metadatalist:
        if parsed_as is None or origutt is None:
            key = meta.attrib['name']
            if key == 'parsed_as':
                parsed_as = meta.attrib['value']
            if key == 'origutt':
                origutt = meta.attrib['value']
    return origutt, parsed_as


def mkmetarecord(meta, origutt, parsed_as):
    if meta is None:
        return None, []
    key = meta.attrib['name']
    if meta.tag == 'xmeta':
        if meta.attrib['source'] in ['CHAT', 'SASTA']:
            newmetarecord = [meta.attrib['name'], meta.attrib['value'], meta.attrib['source'], meta.attrib['cat'],
                             meta.attrib['subcat'], origutt, parsed_as]
            return key, newmetarecord
        else:
            return key, []
    else:
        return key, []


def updateerrordict(errordict, uttid, oldtree, newtree):
    metadatalist = newtree.find(metadataxpath)
    if metadatalist is not None:
        origutt, parsed_as = get_origandparsedas(metadatalist)

        for meta in metadatalist:
            key, newmetarecord = mkmetarecord(meta, origutt, parsed_as)
            if key is not None and newmetarecord != []:
                errordict[key].append([uttid] + newmetarecord)
    return errordict


def correcttreebank(treebank, targets, method, corr=corrn):
    allorandalts = []
    errordict = defaultdict(list)
    if corr == corr0:
        return treebank, errordict, allorandalts
    else:
        newtreebank = etree.Element('treebank')
        errorlogrows = []
        for stree in treebank:
            uttid = getuttid(stree)
            # print(uttid)
            mustbedone = get_mustbedone(stree, targets)
            if mustbedone:
                # to implement
                newstree, orandalts = correct_stree(stree, method, corr)
                if newstree is not None:
                    errordict = updateerrordict(errordict, uttid, stree, newstree)
                    newtreebank.append(newstree)
                    allorandalts.append(orandalts)
                else:
                    newtreebank.append(stree)
            else:
                newtreebank.append(stree)

        return newtreebank, errordict, allorandalts


def contextualise(node1, node2):
    '''
    copies the contextually determined properties of node2 to node1
    :param node1:
    :param node2:
    :return: adapted version of node1
    '''
    newnode = copy(node1)
    for prop in contextualproperties:
        if prop in node2.attrib:
            newnode.attrib[prop] = node2.attrib[prop]
    return newnode


def updatetokenpos(resulttree, tokenposdict):
    # resulttree = deepcopy(stree)
    for child in resulttree:
        newchild = updatetokenpos(child, tokenposdict)
    if ('pt' in resulttree.attrib or 'pos' in resulttree.attrib) and 'end' in resulttree.attrib and 'begin' in resulttree.attrib:
        intend = int(resulttree.attrib['end'])
        if intend in tokenposdict:
            newendint = tokenposdict[intend]
            resulttree.attrib['end'] = str(newendint)
            resulttree.attrib['begin'] = str(newendint - 1)
        else:
            SDLOGGER.error('Correcttreebank:updatetokenpos: Missing key in tokenposdict: key={key}'.format(key=intend))
            #etree.dump(resulttree)
            SDLOGGER.error('tokenposdict={}'.format(tokenposdict))
    elif 'cat' in resulttree.attrib:
        children = [ch for ch in resulttree]
        (b, e) = getbeginend(children)
        resulttree.attrib['begin'] = b
        resulttree.attrib['end'] = e

    return resulttree


def findskippednodes(stree, tokenlist):
    topnode = find1(stree, './/node[@cat="top"]')
    # tokenposdict =  {i+1:tokenlist[i].pos+1 for i in range(len(tokenlist))}
    tokenposdict = {}
    elctr = 0
    i = 0
    for tok in tokenlist:
        elctr += 1
        if not tok.skip:
            tokenposdict[elctr] = i + 1
            i += 1
    resultlist = findskippednodes2(topnode, tokenposdict)
    return resultlist


def findskippednodes2(stree, tokenposdict):
    resultlist = []
    if stree is None:
        return resultlist
    if 'pt' in stree.attrib or 'pos' in stree.attrib:
        if int(stree.attrib['end']) not in tokenposdict:
            resultlist.append(stree)
    elif 'cat' in stree.attrib:
        for child in stree:
            resultlist += findskippednodes2(child, tokenposdict)
    else:
        pass
    return resultlist


def blowup(token):
    result = token.pos * 10 + token.subpos
    return result

def insertskips(newstree, tokenlist, stree):
    '''

    :param newstree: the corrected tree, with skipped elements absent
    :param tokenposlist: list of all tokens with skips marked
    :param stree: original stree with parses of the skipped elements
    :return: adapted tree, with the skipped elements inserted (node from the original stree as -- under top, begin/ends updates
    '''
    #debug = True
    debug = False

    if debug:
        print('\nnewstree:')
        etree.dump(newstree)
    resulttree = deepcopy(newstree)
    # tokenpostree = deepcopy(stree)
    # update begin/ends
    reducedtokenlist = [t for t in tokenlist if not t.skip]
    tokenposdict = {i + 1: blowup(reducedtokenlist[i]) + 1 for i in range(len(reducedtokenlist))}
    #showtree(resulttree, text='in: ')
    resulttree = updatetokenpos(resulttree, tokenposdict)
    #showtree(resulttree, text='out:')
    # tokenpostree = updatetokenpos(tokenpostree, tokenposdict)
    if debug:
        print('\nstree:')
        etree.dump(stree)
        # print('\ntokenpostree:')
        # etree.dump(tokenpostree)
        print('\nresulttree:')
        etree.dump(resulttree)

    # insert skipped elements
    nodestoinsert = findskippednodes(stree, tokenlist)
    nodestoinsertcopies = [deepcopy(n) for n in nodestoinsert]
    # simpleshow(stree)
    topnode = find1(resulttree, './/node[@cat="top"] ')
    topchildren = [ch for ch in topnode]
    allchildren = nodestoinsertcopies + topchildren
    sortedchildren = sorted(allchildren, key=lambda x: x.attrib['end'], reverse=True)
    # simpleshow(stree)
    for ch in topnode:
        topnode.remove(ch)
    # simpleshow(stree)
    for node in sortedchildren:
        node.attrib['rel'] = '--'    # these are now extragrammatical with relation --
        topnode.insert(0, node)
    # simpleshow(stree)
    (b, e) = getbeginend(sortedchildren)
    topnode.attrib['begin'] = b
    topnode.attrib['end'] = e
    # simpleshow(stree)

    sentlist = getyield(resulttree)
    sent = space.join(sentlist)
    sentnode = find1(resulttree, 'sentence')
    sentnode.text = sent
    if debug:
        print('result of insertskips')
        etree.dump(resulttree)

    return resulttree


def correct_stree(stree, method, corr):
    '''

    :param stree: input stree
    :param method:  method (tarsp, asta, stap)
    :param corr: correctionoption
    :return: corrected stree
    '''

    # debug = True
    debug = False
    if debug:
        print('1:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    allmetadata = []
    orandalts = []

    # uttid:
    uttid = getuttid(stree)
    sentid = getsentid(stree)

    # get the original utterance

    origutt = getorigutt(stree)
    if origutt is None:
        SDLOGGER.error('Missing origutt in utterance {}'.format(uttid))
        return stree, orandalts
    # list of token positions

    # get the original metadata; these will be added later to the tree of each correction
    metadatalist = stree.xpath(metadataxpath)
    lmetadatalist = len(metadatalist)
    if lmetadatalist == 0:
        SDLOGGER.error('Missing metadata in utterance {}'.format(uttid))
    elif lmetadatalist > 1:
        SDLOGGER.error('Multiple metadata ({}) in utterance {}'.format(lmetadatalist, uttid))
    else:
        origmetadata = metadatalist[0]

    # allmetadata += origmetadata
    # clean in the tokenized manner

    cleanutt, chatmetadata = cleantext(origutt, False)
    allmetadata += chatmetadata
    cleanutttokens = sasta_tokenize(cleanutt)
    cleanuttwordlist = [t.word for t in cleanutttokens]

    # get corrections, given the stree

    ctmds = getcorrections(cleanutt, method, stree)

    if debug:
        print('2:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    ptmds = []
    for correctiontokenlist, cwmdmetadata in ctmds:
        cwmdmetadata += allmetadata
        correctionwordlist = tokenlist2stringlist(correctiontokenlist, skip=True)

        # parse the corrections
        if correctionwordlist != cleanuttwordlist:
            # @@@adapt this, skip the tokens to be skipped@@@
            # correction = space.join(correctionwordlist)
            correction, tokenposlist = mkuttwithskips(correctiontokenlist)
            cwmdmetadata += [Meta('parsed_as', correction, cat='Correction', source='SASTA')]
            newstree = PARSE_FUNC(correction)
            if newstree is None:
                newstree = stree  # is this what we want?@@
            else:
                # insert the leftout words and adapt the begin/ends of the nodes
                # simpleshow(stree)
                newstree = insertskips(newstree, correctiontokenlist, stree)
                # simpleshow(stree)
                mdcopy = deepcopy(origmetadata)
                newstree.insert(0, mdcopy)
                # copy the sentid attribute
                sentencenode = getsentencenode(newstree)
                if sentencenode is not None:
                    sentencenode.attrib['sentid'] = sentid
                if debug:
                    print(etree.tostring(newstree, pretty_print=True))
                # etree.dump(newstree)

        else:
            # make sure to include the xmeta from CHAT cleaning!! variable allmetadata, or better metadata but perhaps rename to chatmetadata
            newstree = add_metadata(stree, chatmetadata)

        ptmds.append((correctionwordlist, newstree, cwmdmetadata))

    # select the stree for the most promising correction
    if debug:
        print('3:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    if ptmds == []:
        thecorrection, orandalts = (cleanutt, stree, origmetadata), None
    elif corr in [corr1, corrn]:
        thecorrection, orandalts = selectcorrection(stree, ptmds, corr)
    else:
        SDLOGGER.error('Illegal correction value: {}. No corrections applied'.format(corr))
        thecorrection, orandalts = (cleanutt, stree, origmetadata), None

    thetree = deepcopy(thecorrection[1])

    debuga = False
    if debuga:
        print('4: (stree)')
        etree.dump(stree, pretty_print=True)

    # do replacements in the tree
    if debuga:
        print('4b: (thetree)')
        etree.dump(thetree, pretty_print=True)
    reverseposindex = gettokposlist(thetree)

    if debuga:
        print('4b: (thetree)')
        etree.dump(thetree, pretty_print=True)

    # resultposmeta = selectmeta('cleanedtokenpositions', allmetadata)
    # resultposlist = resultposmeta.value

    newcorrection2 = thecorrection[2]
    nodes2deletebegins = []
    for meta in thecorrection[2]:
        if meta.backplacement == bpl_node:
            nodeend = meta.annotationposlist[-1] + 1
            newnode = myfind(thetree, './/node[@pt and @end="{}"]'.format(nodeend))
            oldnode = myfind(stree, './/node[@pt and @end="{}"]'.format(nodeend))
            if newnode is not None and oldnode is not None:
                # adapt oldnode1 for contextual features
                contextoldnode = contextualise(oldnode, newnode)
                thetree = transplant_node(newnode, contextoldnode, thetree)
        elif meta.backplacement == bpl_word or meta.backplacement == bpl_wordlemma:
            nodeend = meta.annotationposlist[-1] + 1
            nodexpath = './/node[@pt and @begin="{}" and @end="{}"]'.format(nodeend - 1, nodeend)
            newnode = myfind(thetree, nodexpath)
            oldnode = myfind(stree, nodexpath)
            if newnode is not None and oldnode is not None:
                if 'word' in newnode.attrib and 'word' in oldnode.attrib:
                    newnode.attrib['word'] = oldnode.attrib['word']
                    thetree = adaptsentence(thetree)
                else:
                    if 'word' not in oldnode.attrib:
                        SDLOGGER.error('Unexpected missing "word" attribute in utterance {}, node'.format(uttid, simpleshow(oldnode, showchildren=False)))
                    if 'word' not in newnode.attrib:
                        SDLOGGER.error('Unexpected missing "word" attribute in utterance {}, node'.format(uttid, simpleshow(oldnode, showchildren=False)))
            if meta.backplacement == bpl_wordlemma:
                if newnode is not None and oldnode is not None:
                    if 'lemma' in newnode.attrib and 'lemma' in oldnode.attrib:
                        newnode.attrib['lemma'] = oldnode.attrib['lemma']
                        thetree = adaptsentence(thetree)
                    else:
                        if 'lemma' not in oldnode.attrib:
                            SDLOGGER.error('Unexpected missing "lemma" attribute in utterance {}, node'.format(uttid, simpleshow(oldnode, showchildren=False)))
                        if 'lemma' not in newnode.attrib:
                            SDLOGGER.error('Unexpected missing "lemma" attribute in utterance {}, node'.format(uttid, simpleshow(oldnode, showchildren=False)))

        elif meta.backplacement == bpl_none:
            pass
        elif meta.backplacement == bpl_delete:
            orignodebegin = str(meta.annotatedposlist[-1])
            nodes2deletebegins.append(orignodebegin)  # just gather the begin sof the nodes to be deleted
        elif meta.backplacement == bpl_indeze:
            nodebegin = meta.annotatedposlist[-1]
            nodeend = nodebegin + 1
            oldnode = myfind(stree, './/node[@pt and @end="{}"]'.format(nodeend))
            if oldnode is not None:
                nodeid = oldnode.attrib['id']
                dezeAVnode = etree.fromstring(dezeAVntemplate.format(begin=nodebegin, end=nodeend, id=nodeid))
                thetree = transplant_node(oldnode, dezeAVnode, thetree)

        #etree.dump(thetree, pretty_print=True)

    # now do all the deletions at once, incl normalisation of begins and ends, and new sentence node
    thetree = deletewordnodes(thetree, nodes2deletebegins)

    #etree.dump(thetree, pretty_print=True)

    # adapt the metadata
    cleantokposlist = [meta.annotationwordlist for meta in newcorrection2 if meta.name == 'cleanedtokenpositions']
    cleantokpos = cleantokposlist[0] if cleantokposlist != [] else []
    insertbegins = [meta.annotatedposlist for meta in newcorrection2 if meta.name == insertion ]
    flatinsertbegins = [str(v) for el in insertbegins for v in el]
    purenodes2deletebegins = [v for v in nodes2deletebegins if v not in flatinsertbegins]
    newcorrection2 = [updatecleantokmeta(meta, purenodes2deletebegins, cleantokpos) for meta in newcorrection2]

    #etree.dump(thetree, pretty_print=True)

    if debug:
        print('5:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    restoredtree = thetree

    # add the metadata to the tree
    fulltree = restoredtree
    # print('dump 1:')
    # etree.dump(fulltree, pretty_print=True)

    metadata = fulltree.find('.//metadata')
    # remove the existing metadata
    if metadata is not None:
        metadata.getparent().remove(metadata)

    # insert the original metadata

    if origmetadata is None:
        metadata = etree.Element('metadata')
        fulltree.insert(0, metadata)
    else:
        fulltree.insert(0, origmetadata)
        metadata = origmetadata

    for meta in newcorrection2:
        metadata.append(meta.toElement())

    if debug:
        streesentlist = getyield(stree)
        fulltreesentlist = getyield(fulltree)
        if streesentlist != fulltreesentlist:
            SDLOGGER.warning('Yield mismatch\nOriginal={original}\nAfter correction={newone}'.format(original=streesentlist,
                                                                                                     newone=fulltreesentlist))

    # return this stree
    # print('dump 2:')
    # etree.dump(fulltree, pretty_print=True)
    return fulltree, orandalts


def getsentencenode(stree):
    sentnodes = stree.xpath('.//sentence')
    if sentnodes == []:
        result = None
    else:
        result = sentnodes[0]
    return result


def updatecleantokmeta(meta, begins, cleantokpos):
    if meta is not None and meta.name in ['cleanedtokenisation', 'cleanedtokenpositions']:
        sortedbegins = sorted(begins, key=lambda x: int(x), reverse=True)
        newmeta = copy(meta)
        for begin in sortedbegins:
            intbegin = int(begin)
            beginindex = cleantokpos.index(intbegin)
            newmeta.annotationwordlist = newmeta.annotationwordlist[:beginindex] \
                + newmeta.annotationwordlist[beginindex + 1:]
        newmeta.value = newmeta.annotationwordlist
        return newmeta
    else:
        return meta


def getuttid(stree):
    uttidlist = stree.xpath(uttidxpath)
    if uttidlist == []:
        SDLOGGER.error('Missing uttid')
        uttid = 'None'
    else:
        uttid = uttidlist[0]
    return uttid


def getorigutt(stree):
    origuttlist = stree.xpath(origuttxpath)
    if origuttlist == []:
        origutt = None
    else:
        origutt = origuttlist[0]
    return origutt


def scorefunction(obj): return (-obj.unknownwordcount, -obj.dpcount, -obj.dhyphencount, obj.goodcatcount,
                                -obj.basicreplaceecount, -obj.hyphencount, obj.dimcount, obj.compcount, obj.supcount,
                                obj.compoundcount, obj.sucount, obj.svaok, -obj.deplusneutcount, -obj.penalty)


class Alternative():
    def __init__(self, stree, altid, altsent, penalty, dpcount, dhyphencount, dimcount,
                 compcount, supcount, compoundcount, unknownwordcount, sucount, svaok, deplusneutcount, goodcatcount,
                 hyphencount, basicreplaceecount):
        self.stree = stree
        self.altid = altid
        self.altsent = altsent
        self.penalty = int(penalty)
        self.dpcount = int(dpcount)
        self.dhyphencount = int(dhyphencount)
        self.dimcount = int(dimcount)
        self.compcount = int(compcount)
        self.supcount = int(supcount)
        self.compoundcount = int(compoundcount)
        self.unknownwordcount = int(unknownwordcount)
        self.sucount = int(sucount)
        self.svaok = int(svaok)
        self.deplusneutcount = int(deplusneutcount)
        self.goodcatcount = int(goodcatcount)
        self.hyphencount = int(hyphencount)
        self.basicreplaceecount = int(basicreplaceecount)

    def alt2row(self, uttid, base, user1='', user2='', user3='', bestaltids=[], selected=None, origsent=None):
        scores = ['BEST'] if self.altid in bestaltids else []
        if self.altid == selected:
            scores.append('SELECTED')
        else:
            scores.append('NOTSELECTED')
        if self.altsent == origsent:
            scores.append('IDENTICAL')
        score = ampersand.join(scores)
        therow = [base, user1, user2, user3] + \
                 ['Alternative', uttid] + 2 * [''] +\
                 [self.altid, self.altsent, score, self.penalty, self.dpcount, self.dhyphencount,
                  self.dimcount, self.compcount, self.supcount, self.compoundcount, self.unknownwordcount, self.sucount,
                  self.svaok, self.deplusneutcount, self.goodcatcount, self.hyphencount, self.basicreplaceecount]
        return therow

    def betterscorethan(self, alt):
        score = {}
        for name, obj in [('self', self), ('alt', alt)]:
            score[name] = scorefunction(obj)
        result = score['self'] > score['alt']
        return result

    def equalscoreas(self, alt):
        score = {}
        for name, obj in [('self', self), ('alt', alt)]:
            score[name] = scorefunction(obj)
        result = score['self'] == score['alt']
        return result


class Original():
    def __init__(self, uttid, stree):
        self.uttid = uttid
        self.stree = stree

    def original2row(self, base, user1='', user2='', user3=''):
        origutt = getorigutt(self.stree)
        origtokenlist = getyield(self.stree)
        origsent = space.join(origtokenlist)
        therow = [base, user1, user2, user3] + \
                 ['Original', self.uttid, origutt, origsent]
        return therow


class OrigandAlts():
    def __init__(self, orig, alts, selected=None):
        self.orig = orig
        self.alts = alts  # a dictionary with altid as key
        self.selected = selected

    def OrigandAlts2rows(self, base, user1='', user2='', user3=''):
        origrow = self.orig.original2row(base, user1, user2, user3)
        origsent = origrow[-1]
        bestaltids = getbestaltids(self.alts)
        altsrows = [self.alts[altid].alt2row(self.orig.uttid, base, user1, user2, user3, bestaltids, self.selected, origsent) for altid in self.alts]
        laltsrows = len(altsrows)
        selectedrow = [base, user1, user2, user3] + \
                      ['Selected', self.orig.uttid, '', self.alts[self.selected].altsent, self.selected]
        if laltsrows > 1:
            rows = [origrow] + altsrows + [selectedrow]
        else:
            rows = []
        return rows


def getbestaltids(alts):
    results = []
    for altid in alts:
        if results == []:
            results = [altid]
        elif alts[altid].betterscorethan(alts[results[0]]):
            results = [altid]
        elif alts[altid].equalscoreas(alts[results[0]]):
            results.append(altid)
    return results


def getsvaokcount(nt):
    subjects = nt.xpath('.//node[@rel="su"]')
    counter = 0
    for subject in subjects:
        pv = find1(subject, '../node[@rel="hd" and @pt="ww" and @wvorm="pv"]')
        if phicompatible(subject, pv):
            counter += 1
    return counter


def getdeplusneutcount(nt):
    theyield = getnodeyield(nt)
    ltheyield = len(theyield)
    counter = 0
    for i in range(ltheyield - 1):
        node1 = theyield[i]
        if getattval(node1, 'lemma') in dets[de]:
            node2 = theyield[i + 1]
            word = getattval(node2, 'word')
            parsedwordtree = PARSE_FUNC(word)
            parsedwordnode = find1(parsedwordtree, './/node[@pt]')
            if parsedwordnode is not None and getattval(parsedwordnode, 'genus') == 'onz' and\
                    getattval(parsedwordnode, 'getal') == 'ev':
                counter += 1
    return counter


validwords = {"z'n"}
punctuationsymbols = """.,?!:;"'"""


def isvalidword(w):
    if known_word(w):
        return True
    elif w in punctuationsymbols:
        return True
    elif w in validwords:
        return True


def selectcorrection(stree, ptmds, corr):
    # to be implemented@@
    # it is presupposed that ptmds is not []

    uttid = getuttid(stree)
    orig = Original(uttid, stree)

    altid = 0
    alts = {}
    for cw, nt, md in ptmds:
        altsent = space.join(cw)
        penalty = compute_penalty(md)
        dpcount = countav(nt, 'rel', 'dp')
        dhyphencount = countav(nt, 'rel', '--')
        dimcount = countav(nt, 'graad', 'dim')
        compcount = countav(nt, 'graad', 'comp')
        supcount = countav(nt, 'graad', 'sup')
        compoundcount = getcompoundcount(nt)
        unknownwordcount = len([w for w in nt.xpath('.//node[@pt!="tsw"]/@lemma') if not(isvalidword(w))])
        sucount = countav(nt, 'rel', 'su')
        svaokcount = getsvaokcount(nt)
        deplusneutcount = getdeplusneutcount(nt)
        goodcatcount = len([node for node in nt.xpath('.//node[@cat and (@cat!="du")]')])
        hyphencount = len([node for node in nt.xpath('.//node[contains(@word, "-")]')])
        basicreplaceecount = len([node for node in nt.xpath('.//node[@word]')
                                  if getattval(node, 'word').lower() in basicreplacements])
        alt = Alternative(stree, altid, altsent, penalty, dpcount, dhyphencount, dimcount, compcount, supcount,
                          compoundcount, unknownwordcount, sucount, svaokcount, deplusneutcount, goodcatcount,
                          hyphencount, basicreplaceecount)
        alts[altid] = alt
        altid += 1
    orandalts = OrigandAlts(orig, alts)

    if corr == corr1:
        orandalts.selected = altid - 1
    else:
        # @@to be implemented@@
        orandalts.selected = altid - 1

    result = ptmds[orandalts.selected]
    return result, orandalts


def compute_penalty(md):
    totalpenalty = 0
    for meta in md:
        totalpenalty += meta.penalty
    return totalpenalty
