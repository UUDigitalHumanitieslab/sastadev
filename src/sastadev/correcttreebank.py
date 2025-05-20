from collections import defaultdict
from copy import copy, deepcopy
from dataclasses import dataclass
from editdistance import distance
import os
from typing import Callable, Dict, List, Optional, Set, Tuple

from lxml import etree

from sastadev.basicreplacements import basicreplacements
from sastadev.cleanCHILDEStokens import cleantext
from sastadev.conf import settings
from sastadev.correctionparameters import CorrectionParameters
from sastadev.corrector import (Correction, disambiguationdict, getcorrections,
                                mkuttwithskips, initialmaarvgxpath)
from sastadev.lexicon import de, dets, known_word, nochildword, nochildwords, validnouns, validword, \
    wordsunknowntoalpinolexicondict, wrongposwordslexicon
from sastadev.macros import expandmacros
from sastadev.metadata import (Meta, bpl_delete, bpl_indeze, bpl_node, bpl_node_nolemma, defaultpenalty,
                               bpl_none, bpl_replacement, bpl_word, bpl_wordlemma, bpl_word_delprec, insertion,
                               SASTA, ADULTSPELLINGCORRECTION, ALLSAMPLECORRECTIONS, BASICREPLACEMENTS, CONTEXT,
                               HISTORY, CHILDRENSPELLINGCORRECTION, THISSAMPLECORRECTIONS, replacementsubsources
                               )
from sastadev.postnominalmodifiers import transformbwinnp, transformppinnp, transformmodRinnp
from sastadev.sastatok import sasta_tokenize
from sastadev.sastatoken import Token, insertinflate, tokenlist2stringlist, tokenlist2string
from sastadev.sastatypes import (AltId, CorrectionMode, ErrorDict, MetaElement,
                                 MethodName, Penalty, Position, PositionStr,
                                 SynTree, Targets, Treebank, UttId)
from sastadev.semantic_compatibility import semincompatiblecount
from sastadev.subcatprefs import getsubcatprefscore
from sastadev.sva import phicompatible
from sastadev.syllablecount import countsyllables
from sastadev.targets import get_mustbedone
from sastadev.treebankfunctions import (adaptsentence, add_metadata, clausecats, countav, deflate,
                                        deletewordnodes, fatparse, find1,
                                        getattval, getbeginend,
                                        getcompoundcount, getneighbourwordnode, getnodeyield, getorigutt,
                                        getptsubclass,
                                        getsentid, getsentence, gettokposlist, getxsid,
                                        getyield, myfind, showflatxml,
                                        showtree, simpleshow, subclasscompatible, transplant_node,
                                        treeinflate, treewithtokenpos,
                                        updatetokenpos)
from sastadev.treetransform import adaptlemmas, transformtagcomma, transformtreeld, transformtreenogeen, \
    transformtreenogde, nognietsplit

ampersand = '&'

positive = +1
negative = -1

subsourcesep = '/'

corr0, corr1, corrn = '0', '1', 'n'
validcorroptions = [corr0, corr1, corrn]

space = ' '
uttidxpath = './/meta[@name="uttid"]/@value'
dezebwxpath = './/node[@pt="bw" and @lemma="deze"]'
# noun1cxpath = './/node[@pt="n" and string-length(@word)=1]'
noun1cxpath = './/node[@pt!="let" and string-length(@word)=1]'
metadataxpath = './/metadata'
dezeAVntemplate = '<node begin="{begin}" buiging="met-e" end="{end}" frame="determiner(de,nwh,nmod,pro,nparg)" ' \
                  'id="{id}" infl="de" lcat="np" lemma="deze" naamval="stan" npagr="rest" pdtype="det" pos="det" ' \
                  'positie="nom" postag="VNW(aanw,det,stan,nom,met-e,rest)" pt="vnw" rel="obj1" root="deze" ' \
                  'sense="deze" vwtype="aanw" wh="nwh" word="deze"/>'

contextualproperties = ['rel', 'index', 'positie']

ParsedCorrection = Tuple[List[str], SynTree, List[Meta]]
TupleNint = Tuple[19 * (int,)]



smartreplacepairs = [('me', 'mijn'), ('ze', 'zijn')]
smartreplacedict = {w1: w2 for w1, w2 in smartreplacepairs}



class Criterion():
    def __init__(self, name, getfunction, polarity, description):
        self.name: str = name
        self.getfunction: Callable[[SynTree], bool] = getfunction
        self.polarity: int = polarity
        self.description: str = description



class Alternative():
    def __init__(self, stree, altid, altsent, criteria):
        self.stree: SynTree = stree
        self.altid: AltId = altid
        self.altsent: str = altsent
        self.criteria = criteria

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
        part4 = list(
            map(str, [self.altid, self.altsent, score] + self.criteria))
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
        # a dictionary with altid as key
        self.alts: Dict[AltId, Alternative] = alts
        self.selected: AltId = selected

    def OrigandAlts2rows(self, base: str, user1: str = '', user2: str = '', user3: str = '') -> List[str]:
        origrow = self.orig.original2row(base, user1, user2, user3)
        origsent = origrow[-1]
        bestaltids = getbestaltids(self.alts)
        altsrows = [
            self.alts[altid].alt2row(
                self.orig.uttid, base, user1, user2, user3, bestaltids, self.selected, origsent)
            for altid in self.alts]
        laltsrows = len(altsrows)
        selectedrow = [base, user1, user2, user3] + \
                      ['Selected', self.orig.uttid, '',
                       self.alts[self.selected].altsent, str(self.selected)]
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


def isrobustnoun(node: SynTree) -> bool:
    pt = getattval(node, 'pt')
    if pt != 'n':
        result = False
    else:
        ntype = getattval(node, 'ntype')
        getal = getattval(node, 'getal')
        graad = getattval(node, 'graad')
        result = ntype == 'both' and getal == 'both' and graad == 'both'
    return result


def issamewordclass(node1, node2):
    pt1 = getattval(node1, 'pt')
    pt2 = getattval(node2, 'pt')
    result = pt1 == pt2
    if result:
        subclass = getptsubclass(pt1)
        if subclass is not None:
            subclass1 = getattval(node1, subclass)
            subclass2 = getattval(node2, subclass)
            result = subclasscompatible(subclass1, subclass2)
    return result


def infpvpair(newnode, node):
    newnodewvorm = getattval(newnode, 'wvorm')
    nodewvorm = getattval(node, 'wvorm')
    result = newnodewvorm == 'inf' and nodewvorm == 'pv'
    return result


def adaptpv(node):
    if getattval(node, 'pt') == 'ww':
        node.attrib['wvorm'] = 'pv'
        node.attrib['pvagr'] = 'mv'
        node.attrib['pvtijd'] = 'tgw'
        node.attrib['postag'] = 'WW(pv,tgw,mv)'


def smartreplace(node: SynTree, word: str, mn: MethodName) -> SynTree:
    '''
    replaces *node* by a different node if the parse of *word* yields a node with a valid word and the same word class and
     if it does not occur in nochildwords;  otherwise by
    a node with *word* and *lemma* attributes replaced by *word*
    :param node:
    :param word:
    :return:
    '''

    wordtree = settings.PARSE_FUNC(word)
    newnode = find1(wordtree, './/node[@pt]')
    newnodept = getattval(newnode, 'pt')
    nodept = getattval(node, 'pt')
    nodelemma = getattval(node, 'lemma')
    newnodelemma = getattval(newnode, 'lemma')
    if isvalidword(word, mn) and \
            issamewordclass(node, newnode) and \
            not isrobustnoun(newnode) and \
            newnodelemma not in nochildwords:
        result = newnode
        if nodept == 'ww' and '_' in nodelemma and newnodelemma in nodelemma and '_' not in newnodelemma:
            # e.g. nodelemma == 'op_hebben', newnodelemma='hebben'
            cpseppos = nodelemma.find('_')
            prt = nodelemma[:cpseppos]
            result.set('lemma', f'{prt}_{newnodelemma}')
        result.set('begin', getattval(node, 'begin'))
        result.set('end', getattval(node, 'end'))
        result.set('rel', getattval(node, 'rel'))
        if 'index' in node.attrib:
            result.set('index', getattval(node, 'index'))
        if infpvpair(newnode, node):
            adaptpv(result)
    else:
        result = copy(node)
        result.attrib['word'] = word
        nodept = getattval(node, 'pt')
        if '_' in node.attrib['lemma'] and countsyllables(word) == 1 and nodept == 'n':
            result.attrib['lemma'] = word
    return result


def mkmetarecord(meta: MetaElement, origutt: Optional[str], parsed_as: Optional[str]) -> Tuple[Optional[str], List[str]]:
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


def correcttreebank(treebank: Treebank, targets: Targets, correctionparameters: CorrectionParameters,
                    corr: CorrectionMode = corrn) -> Tuple[Treebank, ErrorDict, List[Optional[OrigandAlts]]]:

    '''
    The function *correcttreebank* takes as input:

    * treebank: the treebank of the sample, parsed as is.
    * targets: a specification of the utterances that have to be analysed
    * treebankfullname: name of the file that contains the treebank
    * method: the method to be used. Some corrections are method-specific
    * corr: to indicate how the corrections should be done: no corrections at all, all corrections but the last one
     (usually the one with most adaptations) is selected; all  corrections but the best one according to the evaluation  criterion is selected.
    * options: the input parameters for sastadev

    It returns a triple consisting of

    * the corrected treebank
    * an error dictionary: a list of errors detected and how they have been corrected
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
            uttid = getxsid(stree)
            uttno = find1(stree, './/metadata/meta[@name="uttno"]/@value')
            # print(uttid)
            mustbedone = get_mustbedone(stree, targets)
            if mustbedone:
                # to implementf
                sentence = getsentence(stree)
                newstree, orandalts = correct_stree(stree, corr, correctionparameters)
                if newstree is not None:
                    errordict = updateerrordict(
                        errordict, uttid, stree, newstree)
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
    sortedchildren = sorted(
        allchildren, key=lambda x: x.attrib['end'], reverse=True)
    if debug:
        showtree(resulttree, text='insertskips: resulttree:')
    for ch in topnode:
        topnode.remove(ch)
    if debug:
        showtree(resulttree, text='insertskips: resulttree:')
    for node in sortedchildren:
        # these are now extragrammatical with relation --
        node.attrib['rel'] = '--'
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
    from sastadev.CHAT_Annotation import omittedword
    results = []
    for meta in metalist:
        if meta.name == omittedword:
            results += meta.annotatedposlist
    return results


def cleantextdone(metadataelement):
    for meta in metadataelement:
        if meta.tag == 'xmeta' and 'name' in meta.attrib and meta.attrib['name'] == 'cleantext' and \
                'value' in meta.attrib and meta.attrib['value'] == 'done':
            return True
    return False


def correct_stree(stree: SynTree,  corr: CorrectionMode, correctionparameters: CorrectionParameters) \
        -> Tuple[SynTree, Optional[OrigandAlts]]:
    '''

     The function *correct_stree* takes as input:

    * stree: input syntactic structure
    * corr: CorrectionMode (corr0, corr1, corrn)
    * correctionparameters: CorrectionParameters

    and returns a tuple consisting of:

    * the corrected syntactic structure
    * optionally a specification of the original utterance and all alternatives  considered

    The following steps are carried out:

      1. The original utterance, with all CHAT-annotations, is cleaned using the
      function *cleantext* from the module *cleanCHILDEStokens*. This is necessary to
      generate the metadata for the CHAT-annotations, but it can be discarded when the
      original parses use the same *cleantext* function. Currently that is not
      possible yet because the original parsing is done via GrETEL modules,
      which cannot handle complex metadata (xmeta). The result of this operation is a
      list of tokens of type *Token* as defined in the module *sastatoken*. @@add ref@@

      2. Alpino parses are inflated to be able to deal easily with insertions and
      deletions. See below for more details.

      3. The corrections are obtained by calling the function *getcorrections* from the module *corrector*. xx

      4. The corrections may have tokens that are marked with skip=True, in which case
      they  should not be included in the  corrected utterance, so  a corrected
      utterance with these words left out is created.

      5. Each corrected utterance  is parsed, resulting in an inflated syntactic
      structure.

      6. Words that were left out are now introduced into the syntactic structure,
      in such a way that they have no grammatical relations with other words.

      7. The best alternative is selected from among the original utterance and the
      generated corrected utterances by the function *selectcorrection* from the
      module *correcttreebank*.

      8. The original words and sometimes their properties are now substituted for the
      corrections. The exact nature of the replacement is determined by the value of
      the *backplacement* attribute of the metadata. Expansions are not replaced yet,
      because they must be replaced only after the queries have been executed. Nodes
      for words that have to be deleted are collected, but the actual deletion only
      takes place in the next step.

      9. Words that were marked to be deleted are now all deleted, by the function
      tada *deletewordnodes* of the module *treebankfunction*. xx

      10. The metadata are updated and added to the syntactic structure.

      11. During the whole process the mapping between the nodes for words in the
      original syntactic structure and the nodes for words in the syntactic structure
      for the corrected utterance must be perfect. A check is performed to determine
      whether this is the case.

      12. Finally, the corrected syntactic structure and the specification of the
      original utterance and all alternatives considered is returned.

    '''

    # debug = True
    debug = False
    if debug:
        print('1:', end=': ')
        simpleshow(stree)
        print(showflatxml(stree))

    # tree transformations
    if correctionparameters.method in ['tarsp', ' stap']:
        stree = transformtagcomma(stree)
        stree = transformtreeld(stree)
        stree = transformppinnp(stree)
        stree = transformbwinnp(stree)
        stree = transformmodRinnp(stree)
        stree = transformtreenogeen(stree)
        stree = transformtreenogde(stree)
        # stree = nognietsplit(stree)  # put off because it should not be done

    # adapt lemmas for words of which we know Alpino does it wrong
    stree = adaptlemmas(stree)

    allmetadata = []
    # orandalts = []

    # uttid:
    uttid = getxsid(stree)
    sentid = getsentid(stree)

    # get the original utterance

    origutt = getorigutt(stree)
    if origutt is None:
        settings.LOGGER.error('Missing origutt in utterance {}'.format(uttid))
        origutt = space.join(getyield(stree))
        # return stree, orandalts
    # list of token positions

    # get the original metadata; these will be added later to the tree of each correction
    metadatalist = stree.xpath(metadataxpath)
    lmetadatalist = len(metadatalist)
    if lmetadatalist == 0:
        settings.LOGGER.error('Missing metadata in utterance {}'.format(uttid))
        origmetadata = None
    else:
        if lmetadatalist > 1:
            settings.LOGGER.error(
                'Multiple metadata ({}) in utterance {}'.format(lmetadatalist, uttid))
        origmetadata = metadatalist[0]

    # allmetadata += origmetadata
    # clean in the tokenized manner

    cleanutttokens, chatmetadata = cleantext(origutt, False, tokenoutput=True)
    # if not cleantextdone(origmetadata):  # otherwise we get double metadata for cleantext maar werkt niet goed
    #    allmetadata += chatmetadata
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

    rawctmds: List[Correction] = getcorrections(cleanutttokens, correctionparameters, fatstree)

    ctmds = reducecorrections(rawctmds, correctionparameters.method)
    # ctmds = rawctmds

    debug = False
    if debug:
        showtree(fatstree, text='2:')
    debug = False

    fatstreewordlist = getyield(fatstree)
    ptmds = []
    for correctiontokenlist, cwmdmetadata in ctmds:
        cwmdmetadata += allmetadata
        correctionwordlist = tokenlist2stringlist(
            correctiontokenlist, skip=True)

        # parse the corrections
        # if correctionwordlist != cleanuttwordlist and correctionwordlist != []:
        if correctionwordlist != fatstreewordlist and correctionwordlist != []:
            correction, tokenposlist = mkuttwithskips(correctiontokenlist)
            cwmdmetadata += [Meta('parsed_as', correction,
                                  cat='Correction', source='SASTA', penalty=0)]
            reducedcorrectiontokenlist = [
                token for token in correctiontokenlist if not token.skip]
            fatnewstree = fatparse(correction, reducedcorrectiontokenlist)
            debugb = False
            if debugb:
                showtree(fatnewstree, text='fatnewstree')

            if fatnewstree is None:
                fatnewstree = fatstree  # is this what we want?@@
            else:
                # insert the leftout words and adapt the begin/ends of the nodes
                # simpleshow(stree)
                fatnewstree = insertskips(
                    fatnewstree, correctiontokenlist, fatstree)
                # newstree = insertskips(newstree, correctiontokenlist, stree)
                # simpleshow(stree)
                mdcopy = deepcopy(origmetadata)
                if mdcopy is not None:
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

        ptmds.append((correctiontokenlist, fatnewstree, cwmdmetadata))

    # select the stree for the most promising correction
    debug = False
    if debug:
        print('3:', end=': ')
        showtree(fatnewstree)
    debug = False

    if ptmds == []:
        thecorrection, orandalts = (cleanutttokens, fatstree, origmetadata), None
    elif corr in [corr1, corrn]:
        thecorrection, orandalts = selectcorrection(fatstree, ptmds, corr, correctionparameters.method)
    else:
        settings.LOGGER.error(
            'Illegal correction value: {}. No corrections applied'.format(corr))
        thecorrection, orandalts = (cleanutttokens, fatstree, origmetadata), None

    thetree = deepcopy(thecorrection[1])
    correctiontokenlist = thecorrection[0]
    debuga = False
    # debuga = False
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
    if debug:
        showtree(fatstree, text='fatstree')
    nextbackplacement = None
    for mctr, meta in enumerate(thecorrection[2]):
        curbackplacement = nextbackplacement if nextbackplacement is not None else meta.backplacement
        if curbackplacement in [bpl_node, bpl_node_nolemma]:
            nodeend = meta.annotationposlist[-1] + 1
            newnode = myfind(
                thetree, './/node[@pt and @end="{}"]'.format(nodeend))
            oldnode = myfind(
                fatstree, './/node[@pt and @end="{}"]'.format(nodeend))
            if newnode is not None and oldnode is not None:
                # adapt oldnode1 for contextual features
                contextoldnode = contextualise(oldnode, newnode)
                if curbackplacement == bpl_node_nolemma:
                    newnodelemma = getattval(newnode, 'lemma')
                    contextoldnode.set('lemma', newnodelemma)
                thetree = transplant_node(newnode, contextoldnode, thetree)
        elif curbackplacement == bpl_replacement:
            # showtree(fatstree, 'fatstree')
            if len(meta.annotationposlist) > 1:
                pass
            else:
                nodeend = meta.annotationposlist[-1] + 1
                newnode = myfind(
                    thetree, './/node[@pt and @end="{}"]'.format(nodeend))
                oldword = meta.annotatedwordlist[0] if meta.annotatedwordlist != [
                ] else None
                if newnode is None:  # @@todo first check here whether the node is in a left-out retracing part @@
                    settings.LOGGER.error(
                        f'Error in metadata:\n meta={meta}\n No changes applied\nsentence={getsentencenode(thetree).text}')

                if newnode is not None and oldword is not None:
                    # wproplist = getwordinfo(oldword)
                    # wprop = wproplist[0] if wproplist != [] else None
                    # # (pt, dehet, infl, lemma)
                    # newnode.attrib['word'] = oldword
                    # if wprop is None:
                    #    newnode.attrib['lemma'] = oldword
                    # else:
                    #    newnode.attrib['lemma'] = wprop[3]
                    substnode = smartreplace(newnode, oldword, correctionparameters.method)

                    newnodeparent = newnode.getparent()
                    newnodeparent.remove(newnode)
                    newnodeparent.append(substnode)
            # showtree(thetree, 'thetree after smart replace')

        elif curbackplacement in [bpl_word, bpl_wordlemma]:
            nodeend = meta.annotationposlist[-1] + 1
            nodexpath = './/node[@pt and @begin="{}" and @end="{}"]'.format(
                nodeend - 1, nodeend)
            newnode = myfind(thetree, nodexpath)
            oldnode = myfind(fatstree, nodexpath)
            if newnode is not None and oldnode is not None:
                if 'word' in newnode.attrib and 'word' in oldnode.attrib:
                    newnode.attrib['word'] = oldnode.attrib['word']
                    thetree = adaptsentence(thetree)
                else:
                    if 'word' not in oldnode.attrib:
                        settings.LOGGER.error(
                            'Unexpected missing "word" attribute in utterance {}, node: '.format(uttid))
                        simpleshow(oldnode, showchildren=False)
                    if 'word' not in newnode.attrib:
                        settings.LOGGER.error(
                            'Unexpected missing "word" attribute in utterance {}, node: '.format(uttid))
                        simpleshow(oldnode, showchildren=False)
            if curbackplacement == bpl_wordlemma:
                if newnode is not None and oldnode is not None:
                    if 'lemma' in newnode.attrib and 'lemma' in oldnode.attrib:
                        newnode.attrib['lemma'] = oldnode.attrib['lemma']
                        thetree = adaptsentence(thetree)
                    else:
                        if 'lemma' not in oldnode.attrib:
                            settings.LOGGER.error(
                                'Unexpected missing "lemma" attribute in utterance {}, node: '.format(uttid))
                            simpleshow(oldnode, showchildren=False)
                        if 'lemma' not in newnode.attrib:
                            settings.LOGGER.error(
                                'Unexpected missing "lemma" attribute in utterance {}, node {}'.format(uttid, newnode))
                            simpleshow(oldnode, showchildren=False)
        elif curbackplacement == bpl_word_delprec: # this is rather ad-hoc a more principled way will have to be found
            nodeend = meta.annotationposlist[-1] + 1
            nodexpath = './/node[@pt and @begin="{}" and @end="{}"]'.format(
                nodeend - 1, nodeend)
            newnode = myfind(thetree, nodexpath)
            oldnode = myfind(fatstree, nodexpath)
            newnodeparent = newnode.getparent()
            newnodeparent.remove(newnode)
            nextbackplacement = bpl_word



        elif curbackplacement == bpl_none:
            pass
        elif curbackplacement == bpl_delete:
            orignodebegin = str(meta.annotatedposlist[-1])
            # just gather the begin sof the nodes to be deleted
            nodes2deletebegins.append(orignodebegin)
        elif curbackplacement == bpl_indeze:
            nodebegin = meta.annotatedposlist[-1]
            nodeend = nodebegin + 1
            oldnode = myfind(
                fatstree, './/node[@pt and @end="{}"]'.format(nodeend))
            if oldnode is not None:
                nodeid = oldnode.attrib['id']
                dezeAVnode = etree.fromstring(dezeAVntemplate.format(
                    begin=nodebegin, end=nodeend, id=nodeid))
                thetree = transplant_node(oldnode, dezeAVnode, thetree)
        if curbackplacement not in [bpl_word_delprec]:
            nextbackplacement = None
        # etree.dump(thetree, pretty_print=True)

    # now do all the deletions at once, incl adaptation of begins and ends, and new sentence node
    debug = False
    if debug:
        showtree(thetree, text='thetree before deletion:')

    nodes2deleteintbegins = [int(b) for b in nodes2deletebegins]
    thetree = deletewordnodes(thetree, nodes2deleteintbegins, wordsonly=True)

    if debug:
        showtree(thetree, text='thetree after deletion:')

    debug = False

    # adapt the metadata
    cleantokposlist = [
        meta.annotationwordlist for meta in newcorrection2 if meta.name == 'cleanedtokenpositions']
    cleantokpos = cleantokposlist[0] if cleantokposlist != [] else []
    insertbegins = [
        meta.annotatedposlist for meta in newcorrection2 if meta.name == insertion]
    flatinsertbegins = [str(v) for el in insertbegins for v in el]
    purenodes2deletebegins = [
        str(v) for v in nodes2deletebegins if str(v) not in flatinsertbegins]
    newcorrection2 = [updatecleantokmeta(
        meta, purenodes2deletebegins, cleantokpos) for meta in newcorrection2]

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
            settings.LOGGER.warning(
                'Yield mismatch\nOriginal={original}\nAfter correction={newone}'.format(original=streesentlist,
                                                                                        newone=fulltreesentlist))
    rawoldleavenodes = getnodeyield(fatstree)
    omittedwordbegins = getomittedwordbegins(newcorrection2)
    oldleavenodes = [n for n in rawoldleavenodes if int(
        getattval(n, 'begin')) not in omittedwordbegins]
    oldleaves = [getattval(n, 'word') for n in oldleavenodes]
    newleaves = getyield(fulltree)
    uttid = getxsid(stree)
    if debug and oldleaves != newleaves:
        settings.LOGGER.error(
            'Yield mismatch:{uttid}\n:OLD={oldleaves}\nNEW={newleaves}'.format(uttid=uttid, oldleaves=oldleaves,
                                                                               newleaves=newleaves))
    # return this stree
    # print('dump 2:')
    # etree.dump(fulltree, pretty_print=True)

    # tree transformations
    if correctionparameters.method in ['tarsp', ' stap']:
        fulltree = transformtagcomma(fulltree)
        fulltree = transformtreeld(fulltree)
        fulltree = transformppinnp(fulltree)
        fulltree = transformbwinnp(fulltree)
        fulltree = transformmodRinnp(fulltree)
        fulltree = transformtreenogeen(fulltree)
        fulltree = transformtreenogde(fulltree)
        # fulltree = nognietsplit(fulltree) # put off because it should not be done

    # adapt lemmas for words of which we know Alpino does it wrong
    fulltree = adaptlemmas(fulltree)


    # fulltree = deflate(fulltree)  # put off becuase there may be expanded elements
    debug = False
    if debug:
        showtree(fulltree, 'Deflated')

    return fulltree, orandalts


def splitsource(fullsource: str) -> Tuple[str, str]:
    parts = fullsource.split(subsourcesep, maxsplit=2)
    if len(parts) == 2:
        return (parts[0], parts[1])
    elif len(parts) == 1:
        return (parts[0], '')
    else:      #  == 0 or > 2
        # should never occur
        return ('', '')


postcomplsuxpath = """.//node[@rel="su"   and 
                parent::node[@cat="ssub" and not(parent::node[@cat="whsub" or @cat="whrel" or @cat="rel"])] and 
                @begin >= ../node[(@word or @cat) and 
                                  (not(@pdtype) or @pdtype!="adv-pron") and 
                                  (@rel="ld" or @rel="obj1" or @rel="pc" or @rel="obj2")]/@end]"""
def getpostcomplsucount(nt: SynTree, md: List[Meta], mn: MethodName) -> int:
    postcomplsus = nt.xpath(postcomplsuxpath)
    result = len(postcomplsus)
    return result
def getstreereplacementpenalty(stree: SynTree) -> int:
    contextpositions = set()
    spellingcorrectionpositions = set()
    fullpenalty = 0
    metadatas = stree.xpath('.//metadata')
    if metadatas != []:
        metadata = metadatas[0]
        for meta in metadata:
            if meta.tag != 'xmeta':
                continue
            fullsource = meta.attrib['source'] if 'source' in meta.attrib else ''
            mainsource, subsource = splitsource(fullsource)
            if subsource in {BASICREPLACEMENTS, ALLSAMPLECORRECTIONS, HISTORY, CONTEXT, CHILDRENSPELLINGCORRECTION,
                             ADULTSPELLINGCORRECTION, THISSAMPLECORRECTIONS}:
                penalty = meta.attrib['penalty'] if 'penalty' in meta.attrib else 0
                fullpenalty += penalty
                annotatedposlist = meta.attrib['annotatedpositions'] if 'annotatedposlist' in meta.attrib else '[]'
                position = annotatedposlist[1:-1]
                if subsource in [ADULTSPELLINGCORRECTION, CHILDRENSPELLINGCORRECTION] and position != '':
                    spellingcorrectionpositions.add(position)
                if subsource == CONTEXT and position != '':
                    contextpositions.add(position)
        spellcontextintersection = contextpositions.intersection(spellingcorrectionpositions)
        reduction = len(spellcontextintersection) * defaultpenalty
        fullpenalty = fullpenalty - reduction

    return fullpenalty


def getreplacementpenalty(nt: SynTree, mds: List[Meta], mn:MethodName) -> int:
    contextpositions = set()
    spellingcorrectionpositions = set()
    fullpenalty = 0
    for meta in mds:
        fullsource = meta.source
        mainsource, subsource = splitsource(fullsource)
        if subsource in {BASICREPLACEMENTS, ALLSAMPLECORRECTIONS, HISTORY, CONTEXT, CHILDRENSPELLINGCORRECTION,
                         ADULTSPELLINGCORRECTION, THISSAMPLECORRECTIONS}:
            penalty = meta.penalty
            fullpenalty += penalty
            position = meta.annotatedposlist[0] if meta.annotatedposlist != [] else ''
            if subsource in [CHILDRENSPELLINGCORRECTION, ADULTSPELLINGCORRECTION] and position != '':
                spellingcorrectionpositions.add(position)
            if subsource == CONTEXT and position != '':
                contextpositions.add(position)
    spellcontextintersection = contextpositions.intersection(spellingcorrectionpositions)
    reduction = len(spellcontextintersection) * defaultpenalty
    fullpenalty = fullpenalty - reduction

    return fullpenalty

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
        settings.LOGGER.error('Missing uttid')
        uttid = 'None'
    else:
        uttid = uttidlist[0]
    return uttid

def reducecorrections(ctmds: List[Correction], mn:MethodName) -> List[Correction]:
    tempdict = {}
    for tokenlist, metadata in ctmds:
        tokenstr = tokenlist2string(tokenlist)
        newpenalty = compute_penalty(None, metadata, mn)
        if tokenstr in tempdict:
           oldpenalty = tempdict[tokenstr][0]
           if newpenalty < oldpenalty:
               tempdict[tokenstr] = (newpenalty, tokenlist, metadata)
        else:
            tempdict[tokenstr] = (newpenalty, tokenlist, metadata)

    resultlist = []
    for tokenstr in tempdict:
        cand = tempdict[tokenstr]
        result = (cand[1], cand[2])
        resultlist.append(result)

    return resultlist


def scorefunction(obj: Alternative) -> TupleNint:
    return tuple(obj.criteria)


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


def getsvaokcount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    subjects = nt.xpath('.//node[@rel="su"]')
    counter = 0
    for subject in subjects:
        pv = find1(subject, '../node[@rel="hd" and @pt="ww" and @wvorm="pv"]')
        if phicompatible(subject, pv):
            counter += 1
    return counter


def getdeplusneutcount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    theyield = getnodeyield(nt)
    ltheyield = len(theyield)
    counter = 0
    for i in range(ltheyield - 1):
        node1 = theyield[i]
        word1 = getattval(node1, 'word').lower()
        if word1 in dets[de]:
            node2 = theyield[i + 1]
            word2 = getattval(node2, 'word').lower()
            parsedwordtree = settings.PARSE_FUNC(word2)
            parsedwordnode = find1(parsedwordtree, './/node[@pt]')
            if parsedwordnode is not None and getattval(parsedwordnode, 'genus') == 'onz' and \
                    getattval(parsedwordnode, 'getal') == 'ev':
                counter += 1
    return counter


validwords = {"z'n", 'dees', 'cool', "'k"}
punctuationsymbols = """.,?!:;"'"""


def isvalidword(w: str, mn: MethodName, includealpinonouncompound=True) -> bool:
    if nochildword(w):
        return False
    elif validword(w, mn, includealpinonouncompound=includealpinonouncompound):
        return True
    elif w in punctuationsymbols:
        return True
    elif w in validwords:
        return True
    else:
        return False


def countambigwords(stree: SynTree, md:List[Meta], mn:MethodName) -> int:
    leaves = getnodeyield(stree)
    ambignodes = [leave for leave in leaves if getattval(
        leave, 'word').lower() in disambiguationdict]
    result = len(ambignodes)
    return result


def getunknownwordcount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    words = [w for w in nt.xpath('.//node[@pt!="tsw"]/@word')]
    unknownwords = [w for w in words if not isvalidword(w.lower(), mn) ]
    result = len(unknownwords)
    return result

wrongposwordxpathtemplate = './/node[@lemma="{word}" and @pt="{pos}"]'
def getwrongposwordcount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    result = 0
    for word, pos in wrongposwordslexicon:
        wrongposwordxpath = wrongposwordxpathtemplate.format(word=word, pos=pos)
        matches = nt.xpath(wrongposwordxpath)
        result += len(matches)
    return result

sucountxpath = './/node[@rel="su" and not(@pt="ww" and @wvorm="inf") and not(node[@rel="hd" and @pt="ww" and @wvorm="inf"])] '
def getsucount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    matches = nt.xpath(sucountxpath)
    result = len(matches)
    return result

def getdhyphencount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    matches = nt.xpath('.//node[@rel="--" and @pt and @pt!="let"]')
    result = len(matches)
    return result

localgetcompoundcount = lambda nt, md, mn: getcompoundcount(nt)
getdpcount = lambda nt, md, mn: countav(nt, 'rel', 'dp')
# getdhyphencount = lambda nt, md, mn: countav(nt, 'rel', '--')
getdimcount = lambda nt, md, mn: countav(nt, 'graad', 'dim')
getcompcount = lambda nt, md, mn: countav(nt, 'graad', 'comp')
getsupcount = lambda nt, md, mn: countav(nt, 'graad', 'sup')
# getsucount = lambda nt, md, mn: countav(nt, 'rel', 'su')
getbadcatcount = lambda nt, md, mn: len(
    [node for node in nt.xpath('.//node[@cat and (@cat="du") and node[@rel="dp"]]')])
gethyphencount = lambda nt, md, mn: len(
    [node for node in nt.xpath('.//node[contains(@word, "-")]')])
getbasicreplaceecount = lambda nt, md, mn: len([node for node in nt.xpath('.//node[@word]')
                          if getattval(node, 'word').lower() in basicreplacements])
getsubjunctivecount = lambda nt, md, mn: len(
    [node for node in nt.xpath('.//node[@pvtijd="conj"]')])
def getunknownnouncount(nt: SynTree, md:List[Meta], mn: MethodName):
    candidates = nt.xpath('.//node[@pt="n" and @frame="noun(both,both,both)"]')
    realones = [cand for cand in candidates if getattval(cand, 'lemma') not in validnouns]
    result = len(realones)
    return result

getunknownnamecount = lambda nt, md, mn: len([node for node in nt.xpath(
    './/node[@pt="n" and @frame="proper_name(both)"]')])
complsuxpath = expandmacros(""".//node[node[(@rel="ld" or @rel="pc")  and
                                             @end<=../node[@rel="su"]/@begin and @begin >= ../node[@rel="hd"]/@end] and
                                       not(node[%Rpronoun%])]""")
getcomplsucount = lambda nt, md, mn: len([node for node in nt.xpath(complsuxpath)])
getdezebwcount = lambda nt, md, mn: len([node for node in nt.xpath(dezebwxpath)])
getnoun1c_count = lambda nt, md, mn: len([node for node in nt.xpath(noun1cxpath)])


def selectcorrection(stree: SynTree, ptmds: List[ParsedCorrection], corr: CorrectionMode, mn:MethodName) -> Tuple[
    ParsedCorrection, OrigandAlts]:
    # to be implemented@@
    # it is presupposed that ptmds is not []

    uttid = getxsid(stree)
    orig = Original(uttid, stree)

    altid: AltId = 0
    alts: Dict[AltId, Alternative] = {}
    for ct, nt, md in ptmds:
        cw = tokenlist2stringlist(ct)
        altsent = space.join(cw)
        # penalty = compute_penalty(md)

        criteriavalues = [criterion.getfunction(nt, md, mn) * criterion.polarity for criterion in criteria]

        alt = Alternative(stree, altid, altsent, criteriavalues)
        alts[altid] = alt
        altid += 1
    orandalts = OrigandAlts(orig, alts)

    if corr == corr1:
        orandalts.selected = altid - 1
    elif corr == corrn:
        bestaltids = getbestaltids(alts)
        if bestaltids != []:
            bestaltid = bestaltids[0]  # or perhaps better the last one?
        else:
            # should never occur
            theyield: List[str] = getyield(stree)
            utt: str = space.join(theyield)
            settings.LOGGER.error(f'No alternatives for {utt}')
            exit(-1)
        orandalts.selected = bestaltid
    else:
        # should never occur
        settings.LOGGER.error(f'Illegal correction value: {corr}')
        exit(-1)

    result = ptmds[orandalts.selected]
    return result, orandalts

# smainsuxpath = '//node[@cat="smain"  and @begin = node[@rel="su"]/@begin]' # yields unexpected errros (TD12:31; TARSP_08:31)
smainsuxpath =  './/node[@cat="smain" and node[@rel="su"]]'

def countsmainsu(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    matches = nt.xpath(smainsuxpath)
    result = len(matches)
    return result

mainclausexpath = './/node[@cat="smain" or @cat="whq" or (@cat="sv1" and @rel!="body" and @rel!="cnj")]'
def getmainclausecount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    """
    parses with more than 1 main clause node are bad
    :param nt:
    :return:
    """
    matches = nt.xpath(mainclausexpath)
    lmatches = len(matches)
    if lmatches == 1:
        result = 0   # if there is a clause, it is a single main clause what we want
    else:
        result = lmatches
    return result

mainrelxpath = './/node[@rel="--" and (@cat="rel" or @cat="whrel")]'
def mainrelcount(stree: SynTree, md:List[Meta], mn:MethodName) -> int:
    mainrels = stree.xpath(mainrelxpath)
    result = len(mainrels)
    return result


topxpath = './/node[@cat="top"]'
def gettopclause(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    tops = nt.xpath(topxpath)
    if tops == []:
        return 0
    top = tops[0]
    realchildren = [child for child in top if getattval(child, 'pt') not in ['let', 'tsw']]
    if len(realchildren) != 1:
        return 0
    else:
       thechild = realchildren[0]
       thechildcat = getattval(thechild, 'cat')
       result = 1 if thechildcat in clausecats else 0
       return result

toexpath = './/node[@lemma="toe" or (@lemma="tot" and @vztype="fin")]'
naarxpath = './/node[@lemma="naar"]'
def getlonelytoecount(nt: SynTree, md:List[Meta], mn:MethodName) -> int:
    toematches = nt.xpath(toexpath)
    naarmatches = nt.xpath(naarxpath)
    if toematches == []:
        return 0
    if toematches != [] and naarmatches == []:
        return len(toematches)

    result = 0
    for toematch in toematches:
        if all([int(getattval(naarmatch, 'begin')) > int(getattval(toematch, 'begin')) for naarmatch in naarmatches]):
            result += 1
    return result

relasmainsuborderxpath = """.//node[(@cat="rel" or @cat="whrel" )and @rel="--" and 
                            parent::node[@cat="top"] and 
                            node[@rel="body" and @cat="ssub" and .//node[@word]/@end<=node[@rel="hd" and @pt="ww"]/@begin] ]
"""
def getrelasmainsubordercount(nt: SynTree, md: List[Meta], mn: MethodName):
    matches = nt.xpath(relasmainsuborderxpath)
    result = len(matches)
    return result

def compute_penalty(nt: SynTree, md: List[Meta], mn:MethodName) -> Penalty:
    totalpenalty = 0
    for meta in md:
        totalpenalty += meta.penalty
    return totalpenalty

wordsxpath = """.//node[@word]"""
def getnotknownbyalpinocount(nt: SynTree, md: List[Meta], mn: MethodName) -> int:
    wordnodes = nt.xpath(wordsxpath)
    words = [getattval(wordnode, 'word') for wordnode in wordnodes]
    unknownwords = [word for word in words if word in wordsunknowntoalpinolexicondict]
    result = len(unknownwords)
    return result

def gettotaleditdistance(nt: SynTree, md: List[Meta], mn:MethodName) -> int:
    wordlist = getyield(nt)
    totaldistance = 0
    for meta in md:
        fullsource = meta.source
        mainsource, subsource = splitsource(fullsource)
        if subsource in replacementsubsources and \
                len(meta.annotationwordlist) == 1 and \
                len(meta.annotatedwordlist) == 1:
            correctword = meta.annotationwordlist[0]
            wrongword = meta.annotatedwordlist[0]
            dst = distance(wrongword, correctword)
            totaldistance += dst
    return totaldistance

ppinnpxpath = """//node[@cat='pp' and node[@rel='hd' and @lemma!='van'] and parent::node[@cat='np']]"""
def getpostnominalppmodcount(nt: SynTree, md: List[Meta], mn: MethodName) -> int:
    ppinnpmods = nt.xpath(ppinnpxpath)
    result = len(ppinnpmods)
    return result

def getmaaradvcount(nt: SynTree, md: List[Meta], mn: MethodName) -> int:
    initialmaaradvs = nt.xpath(initialmaarvgxpath)
    result = len(initialmaaradvs)
    return result


# The constant *criteria* is a list of objects of class *Criterion* that are used, in the order given, to evaluate parses
criteria = [
    Criterion("unknownwordcount", getunknownwordcount, negative, "Number of unknown words"),
    Criterion('Alpinounknownword', getnotknownbyalpinocount, negative, "Number of words unknown to Alpino"),
    Criterion("wrongposwordcount", getwrongposwordcount, negative, "Number of words with the wrong part of speech"),
    Criterion("unknownnouncount", getunknownnouncount, negative, "Count of unknown nouns according to Alpino"),
    Criterion("unknownnamecount", getunknownnamecount, negative, "Count of unknown names"),
    Criterion('semincompatibilitycount', semincompatiblecount, negative, "Count of the number of semantic incompatibilities"),
    Criterion('maaradvcount', getmaaradvcount, negative, "Count of number of occurrences of clause initial 'maar' as an adverb"),
    Criterion("ambigcount", countambigwords, negative, "Number of ambiguous words"),
    Criterion("dpcount", getdpcount, negative, "Number of nodes with relation dp"),
    Criterion("dhyphencount", getdhyphencount, negative, "Number of nodes with relation --"),
    Criterion("postcomplsucount", getpostcomplsucount, negative,
              "Number of subjects to the right of a complement in a subordinate clause"),
    Criterion('Nominal PP modifier count', getpostnominalppmodcount, negative, "Number of postnominal PP modifiers"),
    Criterion('RelativeMainSuborder', getrelasmainsubordercount, negative, 'Number of Main Relative Clauses with subordinate order'),
    Criterion("lonelytoecount", getlonelytoecount, negative, "Number of occurrences of lonely 'toe'"),
    Criterion("noun1c_count", getnoun1c_count, negative, "Number of nouns that consist of a single character"),
    Criterion('ReplacementPenalty', getreplacementpenalty, negative, 'Plausibility of the replacement'),
    Criterion('Total Edit Distance', gettotaleditdistance, negative, "Total of the edit distances for all replaced words"),
    # Criterion('Subcatscore', getsubcatprefscore, positive,
    #          'Score based on the frequency of the subcategorisation pattern'),  # put off needs revision
    #    Criterion('mainrelcount', mainrelcount, negative, 'Dislike main relative clauses'),  # removed, leads to worse results
    Criterion("mainclausecount", getmainclausecount, negative, "Number of main clauses"),
    Criterion("topclause", gettopclause, positive, "Single clause under top"),
    Criterion("complsucount", getcomplsucount, negative, ""),
    Criterion("badcatcount", getbadcatcount, negative, "Count of bad categories: du that contains a node with relation dp"),
    Criterion("basicreplaceecount", getbasicreplaceecount, negative, "Number of words from the basic replacements"),
    Criterion("hyphencount", gethyphencount, negative, "Number rof words that contain hyphens"),
    Criterion("subjunctivecount", getsubjunctivecount, negative, "Number of subjunctive verb forms"),
    Criterion("smainsucount", countsmainsu, positive, "Count of smain nodes that contain a subject"),
    Criterion("dimcount", getdimcount, positive, "Number of words that are diminutives"),
    Criterion("compcount", getcompcount, positive, "Number of words that are comparatives"),
    Criterion("supcount", getsupcount, positive, "Number of words that are superlatives"),
    Criterion("compoundcount", localgetcompoundcount, positive, "Number of nouns that are compounds"),
    Criterion("sucount", getsucount, positive, "Number of subjects"),
    Criterion("svaok", getsvaokcount, positive, "Number of time subject verb agreement is OK"),
    Criterion("deplusneutcount", getdeplusneutcount, negative, "Number of deviant configuratios with de-determeine + neuiter noun"),
    Criterion("dezebwcount", getdezebwcount, negative, "Count of 'deze' as adverb"),
    Criterion("penalty", compute_penalty, negative, "Penalty for the changes made")
]

altpropertiesheader = [criterion.name for criterion in criteria]

errorwbheader = ['Sample', 'User1', 'User2', 'User3'] + \
                ['Status', 'Uttid', 'Origutt', 'Origsent'] + \
                ['altid', 'altsent', 'score'] + \
                altpropertiesheader
