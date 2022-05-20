from collections import defaultdict
from copy import copy, deepcopy

from lxml import etree

from basicreplacements import basicreplacements
from corrector import Correction, getcorrections, mkuttwithskips, disambiguationdict
from lexicon import de, dets, known_word
from metadata import (Meta, bpl_delete, bpl_indeze, bpl_node, bpl_none,
                      bpl_word, bpl_wordlemma)
from sastatok import sasta_tokenize
from sastatoken import tokenlist2stringlist, Token
from sva import phicompatible
from targets import get_mustbedone
from treebankfunctions import (adaptsentence, add_metadata, countav,
                               deletewordnodes, find1, getattval, getbeginend,
                               getcompoundcount, getnodeyield, getsentid,
                               gettokposlist, getyield, myfind, showflatxml,
                               simpleshow, transplant_node, showtree, treeinflate, fatparse, treewithtokenpos,
                               updatetokenpos, getuttid)
from config import PARSE_FUNC, SDLOGGER
from metadata import insertion
from sastatoken import inflate, deflate, tokeninflate, insertinflate
from CHAT_Annotation import omittedword
from cleanCHILDEStokens import cleantext

from typing import Dict, List, Optional, Set, Sequence, Tuple, Union
from sastatypes import AltId, CorrectionMode, ErrorDict, UttId, MetaElement, MethodName, Penalty, Position, PositionStr, \
    SynTree, Targets, Treebank

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

ParsedCorrection = Tuple[List[str], SynTree, List[Meta]]
Tuple15int = Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]


class Alternative():
    def __init__(self, stree, altid, altsent, penalty, dpcount, dhyphencount, dimcount,
                 compcount, supcount, compoundcount, unknownwordcount, sucount, svaok, deplusneutcount, goodcatcount,
                 hyphencount, basicreplaceecount, ambigcount):
        self.stree: SynTree = stree
        self.altid: AltId = altid
        self.altsent: str = altsent
        self.penalty: Penalty = int(penalty)
        self.dpcount: int = int(dpcount)
        self.dhyphencount: int = int(dhyphencount)
        self.dimcount: int = int(dimcount)
        self.compcount: int = int(compcount)
        self.supcount: int = int(supcount)
        self.compoundcount: int = int(compoundcount)
        self.unknownwordcount: int = int(unknownwordcount)
        self.sucount: int = int(sucount)
        self.svaok: int = int(svaok)
        self.deplusneutcount: int = int(deplusneutcount)
        self.goodcatcount: int = int(goodcatcount)
        self.hyphencount: int = int(hyphencount)
        self.basicreplaceecount: int = int(basicreplaceecount)
        self.ambigcount: int = int(ambigcount)

    def alt2row(self, uttid: UttId, base: str, user1: str = '', user2: str = '', user3: str = '',
                bestaltids: List[AltId] = [],
                selected: Optional[AltId] = None, origsent: Optional[str] = None) -> List[str]:
        scores = ['BEST'] if self.altid in bestaltids else []
        if self.altid == selected:
            scores.append('SELECTED')
        else:
            scores.append('NOTSELECTED')
        if self.altsent == origsent:
            scores.append('IDENTICAL')
        score = ampersand.join(scores)
        part4 = list(map(str, [self.altid, self.altsent, score, self.penalty, self.dpcount, self.dhyphencount,
                               self.dimcount, self.compcount, self.supcount, self.compoundcount, self.unknownwordcount,
                               self.sucount,
                               self.svaok, self.deplusneutcount, self.goodcatcount, self.hyphencount,
                               self.basicreplaceecount]))
        therow: list = [base, user1, user2, user3] + \
                       ['Alternative', uttid] + 2 * [''] + part4

        return therow

    def betterscorethan(self, alt) -> bool:  # looping reference to Alternative needed
        score = {}
        for name, obj in [('self', self), ('alt', alt)]:
            score[name] = scorefunction(obj)
        result = score['self'] > score['alt']
        return result

    def equalscoreas(self, alt) -> bool:
        score = {}
        for name, obj in [('self', self), ('alt', alt)]:
            score[name] = scorefunction(obj)
        result = score['self'] == score['alt']
        return result


class Original():
    def __init__(self, uttid, stree):
        self.uttid: UttId = uttid
        self.stree: SynTree = stree

    def original2row(self, base: str, user1: str = '', user2: str = '', user3: str = '') -> List[str]:
        origutt = getorigutt(self.stree)
        origtokenlist = getyield(self.stree)
        origsent = space.join(origtokenlist)
        theuttid = self.uttid if self.uttid is not None else '??'
        therow = [base, user1, user2, user3] + \
                 ['Original', theuttid, origutt, origsent]
        return therow


class OrigandAlts():
    def __init__(self, orig, alts, selected=0):
        self.orig = orig
        self.alts: Dict[AltId, Alternative] = alts  # a dictionary with altid as key
        self.selected: AltId = selected

    def OrigandAlts2rows(self, base: str, user1: str = '', user2: str = '', user3: str = '') -> List[str]:
        origrow = self.orig.original2row(base, user1, user2, user3)
        origsent = origrow[-1]
        bestaltids = getbestaltids(self.alts)
        altsrows = [
            self.alts[altid].alt2row(self.orig.uttid, base, user1, user2, user3, bestaltids, self.selected, origsent)
            for altid in self.alts]
        laltsrows = len(altsrows)
        selectedrow = [base, user1, user2, user3] + \
                      ['Selected', self.orig.uttid, '', self.alts[self.selected].altsent, str(self.selected)]
        if laltsrows > 1:
            rows = [origrow] + altsrows + [selectedrow]
        else:
            rows = []
        return rows


def get_origandparsedas(metadatalist: List[MetaElement]) -> Tuple[Optional[str], Optional[str]]:
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


def mkmetarecord(meta: MetaElement, origutt: Optional[str], parsed_as: Optional[str]) -> Tuple[
    Optional[str], List[str]]:
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


def updateerrordict(errordict: ErrorDict, uttid: UttId, oldtree: SynTree, newtree: SynTree) -> ErrorDict:
    metadatalist: List[MetaElement] = newtree.find(metadataxpath)
    if metadatalist is not None:
        origutt, parsed_as = get_origandparsedas(metadatalist)

        for meta in metadatalist:
            key, newmetarecord = mkmetarecord(meta, origutt, parsed_as)
            if key is not None and newmetarecord != []:
                errordict[key].append([uttid] + newmetarecord)
    return errordict


def correcttreebank(treebank: Treebank, targets: Targets, method: MethodName, corr: CorrectionMode = corrn) \
        -> Tuple[Treebank, ErrorDict, List[Optional[OrigandAlts]]]:
    '''
    The function *correcttreebank* takes as input:

    * treebank: the treebank of the sample, parsed as is.
    * targets: a specification of the utterances that have to be analysed
    * method: the method to be used. Some corrections are method-specific
    * corr: to indicate how the corrections should be done: no corrections at all, all corrections but the last one (usually the one with most adaptations) is selected; all  corrections but the best one according to the evaluation  criterion is selected.


    It returns a triple consisting of

    * the corrected treebank
    * an error dictionary: a list of errors detected and how they have corrected
    * a list of all original utterances and all alternatives that have been considered

    '''
    allorandalts: List[Optional[OrigandAlts]] = []
    errordict: ErrorDict = defaultdict(list)
    if corr == corr0:
        return treebank, errordict, allorandalts
    else:
        newtreebank: Treebank = etree.Element('treebank')
        # errorlogrows = []
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


def contextualise(node1: SynTree, node2: SynTree) -> SynTree:
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


def updatemetadata(metadata: List[Meta], tokenposdict: Dict[Position, Position]):
    begintokenposdict = {k - 1: v - 1 for (k, v) in tokenposdict.items()}
    newmetadata = []
    for meta in metadata:
        newmeta = deepcopy(meta)
        newmeta.annotationposlist = [begintokenposdict[pos] if pos in begintokenposdict else insertinflate(pos) for pos
                                     in meta.annotationposlist]
        newmeta.annotatedposlist = [begintokenposdict[pos] if pos in begintokenposdict else insertinflate(pos) for pos
                                    in meta.annotatedposlist]
        newmetadata.append(newmeta)
    return newmetadata


def updatetokenposmd(intree: SynTree, metadata: List[Meta], tokenposdict: Dict[Position, Position]):
    resulttree = updatetokenpos(intree, tokenposdict)
    newmetadata = updatemetadata(metadata, tokenposdict)
    return resulttree, newmetadata


def findskippednodes(stree: SynTree, tokenlist: List[Token]) -> List[SynTree]:
    debug = False
    if debug:
        showtree(stree, text='findskippednodes:stree:')
    topnode = find1(stree, './/node[@cat="top"]')
    # tokenposdict =  {i+1:tokenlist[i].pos+1 for i in range(len(tokenlist))}
    tokenposset = {t.pos + 1 for t in tokenlist if not t.skip}
    resultlist = findskippednodes2(topnode, tokenposset)
    return resultlist


def findskippednodes2(stree: SynTree, tokenposset: Set[Position]) -> List[SynTree]:
    resultlist: List[SynTree] = []
    if stree is None:
        return resultlist
    if 'pt' in stree.attrib or 'pos' in stree.attrib:
        if int(stree.attrib['end']) not in tokenposset:
            resultlist.append(stree)
    elif 'cat' in stree.attrib:
        for child in stree:
            resultlist += findskippednodes2(child, tokenposset)
    else:
        pass
    return resultlist


def insertskips(newstree: SynTree, tokenlist: List[Token], stree: SynTree) -> SynTree:
    '''

    :param newstree: the corrected tree, with skipped elements absent
    :param tokenposlist: list of all tokens with skips marked
    :param stree: original stree with parses of the skipped elements
    :return: adapted tree, with the skipped elements inserted (node from the original stree as -- under top, begin/ends updates
    '''
    debug = False

    if debug:
        showtree(newstree, 'newstree:')
        showtree(stree, 'stree')
    reducedtokenlist = [t for t in tokenlist if not t.skip]
    resulttree = treewithtokenpos(newstree, reducedtokenlist)

    if debug:
        showtree(resulttree, text='resulttree:')
    streetokenlist = [t for t in tokenlist if t.subpos == 0]
    stree = treewithtokenpos(stree, streetokenlist)
    if debug:
        showtree(stree, text='stree with tokenpos:')
    debug = False
    # tokenpostree = deepcopy(stree)
    # update begin/ends
    # next not needed anymore
    # tokenposdict = {i + 1: reducedtokenlist[i].pos + 1 for i in range(len(reducedtokenlist))}
    # showtree(resulttree, text='in: ')
    # resulttree, newmetadata = updatetokenposmd(resulttree, metadata, tokenposdict)
    # showtree(resulttree, text='out:')
    # tokenpostree = updatetokenpos(tokenpostree, tokenposdict)
    # if debug:
    # print('\nstree:')
    # etree.dump(stree)
    # # print('\ntokenpostree:')
    # # etree.dump(tokenpostree)
    # print('\nresulttree:')
    # etree.dump(resulttree)

    # insert skipped elements
    nodestoinsert = findskippednodes(stree, tokenlist)
    nodestoinsertcopies = [deepcopy(n) for n in nodestoinsert]
    if debug:
        showtree(stree, text='insertskips: stree:')
    if debug:
        showtree(resulttree, text='insertskips: resulttree:')
    topnode = find1(resulttree, './/node[@cat="top"] ')
    topchildren = [ch for ch in topnode]
    allchildren = nodestoinsertcopies + topchildren
    sortedchildren = sorted(allchildren, key=lambda x: x.attrib['end'], reverse=True)
    if debug:
        showtree(resulttree, text='insertskips: resulttree:')
    for ch in topnode:
        topnode.remove(ch)
    if debug:
        showtree(resulttree, text='insertskips: resulttree:')
    for node in sortedchildren:
        node.attrib['rel'] = '--'  # these are now extragrammatical with relation --
        topnode.insert(0, node)
    if debug:
        showtree(resulttree, text='insertskips: resulttree:')
    (b, e) = getbeginend(sortedchildren)
    topnode.attrib['begin'] = b
    topnode.attrib['end'] = e
    if debug:
        showtree(resulttree, text='insertskips: resulttree:')

    sentlist = getyield(resulttree)
    sent = space.join(sentlist)
    sentnode = find1(resulttree, 'sentence')
    sentnode.text = sent
    if debug:
        showtree(resulttree, 'result of insertskips')

    return resulttree


def getomittedwordbegins(metalist: List[Meta]) -> List[Position]:
    results = []
    for meta in metalist:
        if meta.name == omittedword:
            results += meta.annotatedposlist
    return results


def correct_stree(stree: SynTree, method: MethodName, corr: CorrectionMode) -> Tuple[SynTree, Optional[OrigandAlts]]:
    '''

     The function *correct_stree* takes as input:

    * stree: input syntactic structure
    * method:  MethodName (tarsp, asta, stap)
    * corr: CorrectionMode (corr0, corr1, corrn)

    and returns a tuple consisting of:

    * the corrected syntactic structure
    * optionally a specification of the original utterance and all alternatives  considered

    The following steps are carried out:

    1. The original utterance, with all CHAT-annotations, is cleaned using the function *cleantext* from the module
    *cleanCHILDEStokens*. This is necessary to generate the metadata for the CHAT-annotations, but it can be
    discarded when the original parses use the same *cleantext* function. Currently that is not possible yet because
    the original parsing is done via GrETEL modules, which cannot handle complex metadata (xmeta). The result of
    this operation is a list of tokens of type *Token* as defined in the module *sastatoken*. @@add ref@@

    2. Alpino parses are inflated to be able to deal easily with insertions and deletions. @@add ref@@

    3. The corrections are obtained by calling the function *getcorrections* from the module *corrector*

    4. The corrections may have tokens that are marked with skip=True, in which case they should not be included in the
    corrected utterance, so  a corrected utterance with these words left out is created.

    5. Each corrected utterance  is parsed, resulting in an inflated syntactic structure.

    6. Words that were left out are now introduced into the syntactic structure, in such a way that they have no
    grammatical relations with other words.

    7. The best alternative is selected from among the original utterance and the generated corrected utterances by
    the function *selectcorrection* from the module *correcttreebank*.

    8. The original words and sometimes their properties are now substituted for the corrections. The exact nature of
    the replacement is determined by the value of the *backplacement* attribute of the metadata. Expansions are not
    replaced yet, because they must be replaced only after the queries have been executed. Nodes for words that have
    to be deleted are collected, but the actual deletion only takes place in the next step.

    9. Words that were marked to be deleted are now all deleted, by the function *deletewordnodes* of the module
    *treebankfunction*.

    10. The metadata are updated and added to the syntactic structure.

    11. During the whole process the mapping between the nodes for words in the original syntactic structure and the
    nodes for words in the syntactic structure for the corrected utterance must be perfect. A check is performed
    to determine whether this is the case.

    12. Finally, the corrected syntactic structure and the specification of the original utterance and all alternatives
    considered is returned.

    '''

    # debug = True
    debug = False
    if debug:
        print('1:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    allmetadata = []
    # orandalts = []

    # uttid:
    uttid = getuttid(stree)
    sentid = getsentid(stree)

    # get the original utterance

    origutt = getorigutt(stree)
    if origutt is None:
        SDLOGGER.error('Missing origutt in utterance {}'.format(uttid))
        origutt = space.join(getyield(stree))
        # return stree, orandalts
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

    cleanutttokens, chatmetadata = cleantext(origutt, False, tokenoutput=True)
    allmetadata += chatmetadata
    # cleanutttokens = sasta_tokenize(cleanutt)
    cleanuttwordlist = [t.word for t in cleanutttokens]
    cleanutt = space.join(cleanuttwordlist)

    # get corrections, given the inflated stree
    # inflate the tree
    fatstree = deepcopy(stree)
    treeinflate(fatstree)
    # adapt the begins and ends  in the tree based on the token positions
    debug = False
    if debug:
        showtree(fatstree, text='fatstree voor:')
    tokenlist = [t for t in cleanutttokens]
    fatstree = treewithtokenpos(fatstree, tokenlist)
    if debug:
        showtree(fatstree, text='fatstree na:')
    debug = False
    # (fatstree, text='fattened tree:')

    ctmds: List[Correction] = getcorrections(cleanutttokens, method, fatstree)

    debug = False
    if debug:
        showtree(fatstree, text='2:')
    debug = False

    ptmds = []
    for correctiontokenlist, cwmdmetadata in ctmds:
        cwmdmetadata += allmetadata
        correctionwordlist = tokenlist2stringlist(correctiontokenlist, skip=True)

        # parse the corrections
        if correctionwordlist != cleanuttwordlist and correctionwordlist != []:
            correction, tokenposlist = mkuttwithskips(correctiontokenlist)
            cwmdmetadata += [Meta('parsed_as', correction, cat='Correction', source='SASTA')]
            reducedcorrectiontokenlist = [token for token in correctiontokenlist if not token.skip]
            fatnewstree = fatparse(correction, reducedcorrectiontokenlist)
            debugb = False
            if debugb:
                showtree(fatnewstree, text='fatnewstree')

            if fatnewstree is None:
                fatnewstree = fatstree  # is this what we want?@@
            else:
                # insert the leftout words and adapt the begin/ends of the nodes
                # simpleshow(stree)
                fatnewstree = insertskips(fatnewstree, correctiontokenlist, fatstree)
                # newstree = insertskips(newstree, correctiontokenlist, stree)
                # simpleshow(stree)
                mdcopy = deepcopy(origmetadata)
                fatnewstree.insert(0, mdcopy)
                # copy the sentid attribute
                sentencenode = getsentencenode(fatnewstree)
                if sentencenode is not None:
                    sentencenode.attrib['sentid'] = sentid
                if debugb:
                    showtree(fatnewstree)
                # etree.dump(fatnewstree)

        else:
            # make sure to include the xmeta from CHAT cleaning!! variable allmetadata, or better metadata but perhaps rename to chatmetadata
            fatnewstree = add_metadata(fatstree, chatmetadata)

        ptmds.append((correctionwordlist, fatnewstree, cwmdmetadata))

    # select the stree for the most promising correction
    debug = False
    if debug:
        print('3:', end=': ')
        showtree(fatnewstree)
    debug = False

    if ptmds == []:
        thecorrection, orandalts = (cleanutt, fatstree, origmetadata), None
    elif corr in [corr1, corrn]:
        thecorrection, orandalts = selectcorrection(fatstree, ptmds, corr)
    else:
        SDLOGGER.error('Illegal correction value: {}. No corrections applied'.format(corr))
        thecorrection, orandalts = (cleanutt, fatstree, origmetadata), None

    thetree = deepcopy(thecorrection[1])

    # debuga = True
    debuga = False
    if debuga:
        print('4: (fatstree)')
        etree.dump(fatstree, pretty_print=True)

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
    nodes2deletebegins: List[PositionStr] = []
    # next adapted, the tree is fat already
    debug = False
    if debug:
        showtree(thetree, text='thetree before treewithtokenpos')
    thetree = treewithtokenpos(thetree, correctiontokenlist)
    if debug:
        showtree(thetree, text='thetree after treewithtokenpos')
    for meta in thecorrection[2]:
        if meta.backplacement == bpl_node:
            nodeend = meta.annotationposlist[-1] + 1
            newnode = myfind(thetree, './/node[@pt and @end="{}"]'.format(nodeend))
            oldnode = myfind(fatstree, './/node[@pt and @end="{}"]'.format(nodeend))
            if newnode is not None and oldnode is not None:
                # adapt oldnode1 for contextual features
                contextoldnode = contextualise(oldnode, newnode)
                thetree = transplant_node(newnode, contextoldnode, thetree)
        elif meta.backplacement == bpl_word or meta.backplacement == bpl_wordlemma:
            nodeend = meta.annotationposlist[-1] + 1
            nodexpath = './/node[@pt and @begin="{}" and @end="{}"]'.format(nodeend - 1, nodeend)
            newnode = myfind(thetree, nodexpath)
            oldnode = myfind(fatstree, nodexpath)
            if newnode is not None and oldnode is not None:
                if 'word' in newnode.attrib and 'word' in oldnode.attrib:
                    newnode.attrib['word'] = oldnode.attrib['word']
                    thetree = adaptsentence(thetree)
                else:
                    if 'word' not in oldnode.attrib:
                        SDLOGGER.error('Unexpected missing "word" attribute in utterance {}, node: '.format(uttid))
                        simpleshow(oldnode, showchildren=False)
                    if 'word' not in newnode.attrib:
                        SDLOGGER.error('Unexpected missing "word" attribute in utterance {}, node: '.format(uttid))
                        simpleshow(oldnode, showchildren=False)
            if meta.backplacement == bpl_wordlemma:
                if newnode is not None and oldnode is not None:
                    if 'lemma' in newnode.attrib and 'lemma' in oldnode.attrib:
                        newnode.attrib['lemma'] = oldnode.attrib['lemma']
                        thetree = adaptsentence(thetree)
                    else:
                        if 'lemma' not in oldnode.attrib:
                            SDLOGGER.error('Unexpected missing "lemma" attribute in utterance {}, node: '.format(uttid))
                            simpleshow(oldnode, showchildren=False)
                        if 'lemma' not in newnode.attrib:
                            SDLOGGER.error(
                                'Unexpected missing "lemma" attribute in utterance {}, node {}'.format(uttid))
                            simpleshow(oldnode, showchildren=False)

        elif meta.backplacement == bpl_none:
            pass
        elif meta.backplacement == bpl_delete:
            orignodebegin = str(meta.annotatedposlist[-1])
            nodes2deletebegins.append(orignodebegin)  # just gather the begin sof the nodes to be deleted
        elif meta.backplacement == bpl_indeze:
            nodebegin = meta.annotatedposlist[-1]
            nodeend = nodebegin + 1
            oldnode = myfind(fatstree, './/node[@pt and @end="{}"]'.format(nodeend))
            if oldnode is not None:
                nodeid = oldnode.attrib['id']
                dezeAVnode = etree.fromstring(dezeAVntemplate.format(begin=nodebegin, end=nodeend, id=nodeid))
                thetree = transplant_node(oldnode, dezeAVnode, thetree)

        # etree.dump(thetree, pretty_print=True)

    # now do all the deletions at once, incl adaptation of begins and ends, and new sentence node
    debug = False
    if debug:
        showtree(thetree, text='thetree before deletion:')

    nodes2deleteintbegins = [int(b) for b in nodes2deletebegins]
    thetree = deletewordnodes(thetree, nodes2deleteintbegins)

    if debug:
        showtree(thetree, text='thetree after deletion:')

    debug = False

    # adapt the metadata
    cleantokposlist = [meta.annotationwordlist for meta in newcorrection2 if meta.name == 'cleanedtokenpositions']
    cleantokpos = cleantokposlist[0] if cleantokposlist != [] else []
    insertbegins = [meta.annotatedposlist for meta in newcorrection2 if meta.name == insertion]
    flatinsertbegins = [str(v) for el in insertbegins for v in el]
    purenodes2deletebegins = [str(v) for v in nodes2deletebegins if str(v) not in flatinsertbegins]
    newcorrection2 = [updatecleantokmeta(meta, purenodes2deletebegins, cleantokpos) for meta in newcorrection2]

    # etree.dump(thetree, pretty_print=True)

    if debug:
        showtree(fatstree, text='5:')

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
        streesentlist = getyield(fatstree)
        fulltreesentlist = getyield(fulltree)
        if streesentlist != fulltreesentlist:
            SDLOGGER.warning(
                'Yield mismatch\nOriginal={original}\nAfter correction={newone}'.format(original=streesentlist,
                                                                                        newone=fulltreesentlist))
    rawoldleavenodes = getnodeyield(fatstree)
    omittedwordbegins = getomittedwordbegins(newcorrection2)
    oldleavenodes = [n for n in rawoldleavenodes if int(getattval(n, 'begin')) not in omittedwordbegins]
    oldleaves = [getattval(n, 'word') for n in oldleavenodes]
    newleaves = getyield(fulltree)
    uttid = getuttid(stree)
    if debug and oldleaves != newleaves:
        SDLOGGER.error(
            'Yield mismatch:{uttid}\n:OLD={oldleaves}\nNEW={newleaves}'.format(uttid=uttid, oldleaves=oldleaves,
                                                                               newleaves=newleaves))
    # return this stree
    # print('dump 2:')
    # etree.dump(fulltree, pretty_print=True)
    return fulltree, orandalts


def getsentencenode(stree: SynTree) -> SynTree:
    sentnodes = stree.xpath('.//sentence')
    if sentnodes == []:
        result = None
    else:
        result = sentnodes[0]
    return result


def updatecleantokmeta(meta: Meta, begins: List[str], cleantokpos: List[int]) -> Meta:
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


def oldgetuttid(stree: SynTree) -> UttId:
    uttidlist = stree.xpath(uttidxpath)
    if uttidlist == []:
        SDLOGGER.error('Missing uttid')
        uttid = 'None'
    else:
        uttid = uttidlist[0]
    return uttid


def getorigutt(stree: SynTree) -> Optional[str]:
    origuttlist = stree.xpath(origuttxpath)
    if origuttlist == []:
        origutt = None
    else:
        origutt = origuttlist[0]
    return origutt


def scorefunction(obj: Alternative) -> Tuple15int:
    return (-obj.unknownwordcount, -obj.dpcount, -obj.dhyphencount, obj.goodcatcount,
            -obj.basicreplaceecount, -obj.ambigcount, -obj.hyphencount, obj.dimcount, obj.compcount, obj.supcount,
            obj.compoundcount, obj.sucount, obj.svaok, -obj.deplusneutcount, -obj.penalty)


def getbestaltids(alts: Dict[AltId, Alternative]) -> List[AltId]:
    results: List[AltId] = []
    for altid in alts:
        if results == []:
            results = [altid]
        elif alts[altid].betterscorethan(alts[results[0]]):
            results = [altid]
        elif alts[altid].equalscoreas(alts[results[0]]):
            results.append(altid)
    return results


def getsvaokcount(nt: SynTree) -> int:
    subjects = nt.xpath('.//node[@rel="su"]')
    counter = 0
    for subject in subjects:
        pv = find1(subject, '../node[@rel="hd" and @pt="ww" and @wvorm="pv"]')
        if phicompatible(subject, pv):
            counter += 1
    return counter


def getdeplusneutcount(nt: SynTree) -> int:
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
            if parsedwordnode is not None and getattval(parsedwordnode, 'genus') == 'onz' and \
                    getattval(parsedwordnode, 'getal') == 'ev':
                counter += 1
    return counter


validwords = {"z'n"}
punctuationsymbols = """.,?!:;"'"""


def isvalidword(w: str) -> bool:
    if known_word(w):
        return True
    elif w in punctuationsymbols:
        return True
    elif w in validwords:
        return True
    else:
        return False


def countambigwords(stree: SynTree) -> int:
    leaves = getnodeyield(stree)
    ambignodes = [leave for leave in leaves if getattval(leave, 'word').lower() in disambiguationdict]
    result = len(ambignodes)
    return result


def selectcorrection(stree: SynTree, ptmds: List[ParsedCorrection], corr: CorrectionMode) -> Tuple[
    ParsedCorrection, OrigandAlts]:
    # to be implemented@@
    # it is presupposed that ptmds is not []

    uttid = getuttid(stree)
    orig = Original(uttid, stree)

    altid: AltId = 0
    alts: Dict[AltId, Alternative] = {}
    for cw, nt, md in ptmds:
        altsent = space.join(cw)
        penalty = compute_penalty(md)
        dpcount = countav(nt, 'rel', 'dp')
        dhyphencount = countav(nt, 'rel', '--')
        dimcount = countav(nt, 'graad', 'dim')
        compcount = countav(nt, 'graad', 'comp')
        supcount = countav(nt, 'graad', 'sup')
        compoundcount = getcompoundcount(nt)
        unknownwordcount = len([w for w in nt.xpath('.//node[@pt!="tsw"]/@lemma') if not (isvalidword(w))])
        sucount = countav(nt, 'rel', 'su')
        svaokcount = getsvaokcount(nt)
        deplusneutcount = getdeplusneutcount(nt)
        goodcatcount = len([node for node in nt.xpath('.//node[@cat and (@cat!="du")]')])
        hyphencount = len([node for node in nt.xpath('.//node[contains(@word, "-")]')])
        basicreplaceecount = len([node for node in nt.xpath('.//node[@word]')
                                  if getattval(node, 'word').lower() in basicreplacements])
        ambigwordcount = countambigwords(nt)
        alt = Alternative(stree, altid, altsent, penalty, dpcount, dhyphencount, dimcount, compcount, supcount,
                          compoundcount, unknownwordcount, sucount, svaokcount, deplusneutcount, goodcatcount,
                          hyphencount, basicreplaceecount, ambigwordcount)
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


def compute_penalty(md: List[Meta]) -> Penalty:
    totalpenalty = 0
    for meta in md:
        totalpenalty += meta.penalty
    return totalpenalty
