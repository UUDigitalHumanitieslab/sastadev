from typing import Callable, List, Optional, Tuple

from sastadev.asta_queries import asta_delpv
from sastadev.basicreplacements import is_pronominal_adverb
from sastadev.celexlexicon import celex2dcoimap
from sastadev.conf import settings
from sastadev.CHAT_Annotation import CHAT_replacement, CHAT_wordnoncompletion
from sastadev import correctionlabels
from sastadev.deregularise import correctinflection, overgen, wrongovergen
from sastadev.imperatives import wx, imperatives
from sastadev.lexicon import vuwordslexicon, getwordposinfo, informlexicon
from sastadev.macros import expandmacros
from sastadev.metadata import Meta
from sastadev.missing_det import get_missing_det
# from sastadev.sasta_explanation import get_prefix_and_core
from sastadev.sastatypes import SynTree
from sastadev.stringfunctions import punctuationchars
from sastadev.tblex import get_aanloop_and_core
from sastadev.treebankfunctions import (adjacent, find1, get_left_siblings,
                                        getattval, get_node, getnodeyield, get_word, mdbasedquery,
                                        mdnameonlyxpathtemplate, parent)

gav = getattval

comma = ','

articles = ['de', 'een', 'het', "'t", "'n"]

infl_error_xpath = f""".//xmeta[@name="{correctionlabels.morphologicalerror}" and 
                                (@value="{overgen}" or @value="{wrongovergen}")]"""

morph_error_xpath = f""".//xmeta[@name="{correctionlabels.morphologicalerror}" ]"""


nietxpath = './/node[@lemma="niet"]'
wordxpath = './/node[@pt]'

vzn1basexpath = './/node[ @cat="pp" and (node[@pt="vz"] and node[(@pt="n" or @pt="vnw") and not (%Rpronoun%) and @rel="obj1"] and not(node[@pt="vz" and @vztype="fin"]))]'
vzn1xpath = expandmacros(vzn1basexpath)
vzn2xpath = './/node[node[@lemma="in" and @rel="mwp"] and node[@lemma="deze" and @rel="mwp"]]'
vzn3xpath = './/node[@pt="vz" and ../node[(@lemma="dit" or @lemma="dat")  and @begin>=../node[@pt="vz"]/@end and count(node)<=3] ]'
#vzn4basexpath = './/node[node[@pt="vz" and @rel="hd" and ../node[%Rpronoun% and @rel="obj1" and @end <= ../node[@rel="hd"]/@begin]]]'
#vzn4xpath = expandmacros(vzn4basexpath)

#: The constant *voslahbijxpath* selects nodes (PPs) that contain an adposition and an R-pronoun or a index node
#: coindexed with an R-pronoun.
#:
#: **Remark** It is not actually checked whether the indexed node has an R-pronoun as its antecedent
#:
#: **Remark** We may have to do something special for *pobj1*
#:
voslashbijxpath = expandmacros(""".//node[node[@pt="vz" and @rel="hd"] and
            node[@rel="obj1" and
                 ((@index and not(@word or @cat)) or
                  (%Rpronoun%)
                 )]]""")

#: The constant *vobijxpath* uses the macro *Vobij* to identify adverbial pronouns.
#: The macro **Vobij** is defined as follows::
#:
#:   Vobij = """(@pt="bw" and (contains(@frame,"er_adverb" ) or contains(@frame, "tmp_adverb") or @lemma="daarom") and
#:               @lemma!="er" and @lemma!="daar" and @lemma!="hier" and @lemma!="waar" and
#:               (starts-with(@lemma, 'er') or starts-with(@lemma, 'daar') or
#                 starts-with(@lemma, 'hier') or starts-with(@lemma, 'waar'))
#:              )"""
#:
vobijxpath = expandmacros('.//node[%Vobij%]')


mvznxpath = """.//node[@pt = "n" and  @getal ="mv"]"""
mvznsuffixes = ['en', 'e', 's', 'n']

verklxpath = expandmacros(""".//node[(@pt="n" and @graad="dim" and not(%nodimlemma%)) or %extradimlemma%]""")
verklsuffixes = ['je', 'jes', 'ie', 'ies', 'ke', 'kes']

sva_error_xpath = f""".//xmeta[@name="{correctionlabels.grammarerror}" and @value="{correctionlabels.svaerror}"]"""
regional_pv_variants = [('heb', 'heeft')]
regular_pv_variants = [('kun', 'kan')]

def notadjacent(n1, n2, t): return not adjacent(n1, n2, t)


def xneg(stree):
    nodepairs = []
    nietnodes = stree.xpath(nietxpath)
    for nietnode in nietnodes:
        pnietnode = parent(nietnode)
        leftnietsiblings = get_left_siblings(nietnode)
        leftsiblings = get_left_siblings(pnietnode)
        ppnietnode = parent(pnietnode)
        if getattval(pnietnode, 'cat') == "advp" and len(leftsiblings) == 1 and getattval(ppnietnode, 'rel') == '--':
            result = True
            theleftsibling = leftsiblings[0]
        elif getattval(pnietnode, 'cat') != "advp" and getattval(pnietnode, 'rel') == '--' and len(leftnietsiblings) == 1:
            result = True
            theleftsibling = leftnietsiblings[0]
        else:
            result = False
            theleftsibling = None
        if result:
            nodepairs.append((theleftsibling, nietnode))
    if nodepairs == []:
        return None
    else:
        return nodepairs[0]


def xneg_neg(stree):
    (x, neg) = xneg(stree)
    return neg


def xneg_x(stree):
    (x, neg) = xneg(stree)
    return x


def VzN(stree):
    results = []
    results += stree.xpath(vzn1xpath)
    results += stree.xpath(vzn2xpath)
    results += stree.xpath(vzn3xpath)
    #results += stree.xpath(vzn4xpath) # does not belong here after all, these will be scored under Vo/Bij
    return results


def auxvobij(stree: SynTree, pred: Callable[[SynTree, SynTree, SynTree], bool]) -> List[SynTree]:
    """

    :param stree: the syntactic structure to be analysed
    :param pred: a predicate that the results found must satisfy
    :return: a list of matching nodes

    The function *auxvobij* finds nodes that are found by the *voslashbijxpath* and selects from these those
    that satisfy the predicate *pred*. It is used to distinguish cases of R-pronoun + adposition that are *adjacent*
    (which should be analysed as TARSP *Vobij*) from those that are not adjacent (which should be analysed as TARSP
    Vo/Bij).

    .. autodata:: sastadev.queryfunctions::voslashbijxpath

    """
    RPnodes = stree.xpath(voslashbijxpath)
    results = []
    for RPnode in RPnodes:
        # find the head node
        headnode = find1(RPnode, 'node[@rel="hd"]')

        # find the obj1node
        obj1node = find1(RPnode, 'node[@rel="obj1"]')

        if headnode is not None and obj1node is not None:
            if pred(obj1node, headnode, stree):
                results.append(RPnode)
    return results


def vobij(stree: SynTree) -> List[SynTree]:
    '''

    :param stree: syntactic structure to be analysed
    :return: List of matching nodes

    The function *vobij* uses the Xpath expression *vobijxpath* and the function *auxvobij* to obtain its resulting nodes:

    * The *vobijxpath* expression matches with so-called adverbial pronouns:

      .. autodata:: sastadev.queryfunctions::vobijxpath

    * The function *auxvobij*  finds adjacent R-pronoun + adposition cases:

      .. autofunction:: sastadev.queryfunctions::auxvobij

    '''
    results1 = stree.xpath(vobijxpath)
    results2 = auxvobij(stree, vobijpred)
    results = results1 + results2
    return results


def voslashbij(stree: SynTree) -> List[SynTree]:
    '''

    :param stree: syntactic structuire to be analysed
    :return: List of matching nodes

    The function *voslashbij* uses the function *auxvobij* to find non-adjacent R-pronoun + adposition cases:

    .. autofunction:: sastadev.queryfunctions::auxvobij
          :noindex:


    '''
    results = auxvobij(stree, notadjacent)
    return results

def vobijpred(obj1node, headnode, stree) -> bool:
    #check for adjacency  (er naar is ok, er gisteren naar not)
    cond1 = adjacent(headnode, obj1node, stree)

    # check whether the obj1node precedes the headnode: daar naar is ok, naar daar is not ok
    headposition = int(getattval(headnode, 'end'))
    obj1position = int(getattval(obj1node, 'end'))
    cond2 = obj1position < headposition
    result = cond1 and cond2
    return result


def hequery(syntree: SynTree) -> List[SynTree]:
    """

    :param syntree:
    :return: the node for hè or he, sentence final or prefinal and followed by a punctuation sign
    """
    henodes = syntree.xpath('.//node[@lemma="hè" or @lemma="he"]')
    if henodes != []:
        henode = max(henodes, key=lambda node: int(getattval(node, 'end')))
        nodeyield = getnodeyield(syntree)
        barenodeyield = [node for node in nodeyield if getattval(node, 'pt') != 'let']
        result = [henode] if henode == barenodeyield[
            -1] else []  # the found node must be the last one if punctuation is removed
    else:
        result = []
    return result


vudiversxpath = """
.// node[(@ lemma != "ja" and @ lemma != "nee" and @ word != "xxx" and @ lemma != "mama" and @ word != "xx" and
         (( @ pt="tsw" ) or
          ((@ lemma="au" or @ lemma="hoepla" or @ lemma="dag" or @ lemma="kijk" or @ lemma="hap" or @ lemma="aai") and
           (@ rel="--" or @ rel="sat" or @ rel="tag")
		  )
         ) 
		) or %Tarsp_kijkVU% or %Tarsp_hehe% or %dankje_VU%
    ]
"""
def vudivers(syntree: SynTree) -> List[SynTree]:
    expandedvudiversxpath = expandmacros(vudiversxpath)
    rawresults = syntree.xpath(expandedvudiversxpath)
    vuresults = aanloopuitloopvu(syntree)
    allrawresults = rawresults + [node for node in vuresults if node not in rawresults]
    heresults = hequery(syntree)
    results = [result for result in allrawresults if result not in heresults]
    return results

def tarsp_mvzn(stree: SynTree) -> List[SynTree]:
     mvzns = stree.xpath(mvznxpath)
     realmvzns = [mvzn for mvzn in mvzns if any([mvzn.attrib['word'].endswith(suf) for suf in mvznsuffixes])]
     return realmvzns

def tarsp_verkl(stree: SynTree) -> List[SynTree]:
    verkls = stree.xpath(verklxpath)
    realverkls = [verkl for verkl in verkls if any([verkl.attrib['word'].endswith(suf) for suf in verklsuffixes])]
    return realverkls



def getuitloop(nodeyield: List[SynTree]) -> Tuple[List[SynTree], List[SynTree]]:
    lastlemma = getattval(nodeyield[-1], 'lemma') if nodeyield != [] else ''
    if lastlemma in punctuationchars:
        if lastlemma == comma:
            return nodeyield, []
        elif len(nodeyield) >= 3:
            potential_uitloop = [-3, -2]
        else:
            return nodeyield, []
    elif len(nodeyield) >= 2:
        potential_uitloop = [-2, -1]
    else:
        return nodeyield, []
    lemma1 = getattval(nodeyield[potential_uitloop[0]], 'lemma')
    lemma2 = getattval(nodeyield[potential_uitloop[1]], 'lemma')
    if lemma2 in vuwordslexicon and \
        lemma1 == comma and \
        '3' in vuwordslexicon[lemma2] and \
        comma in vuwordslexicon[lemma2]:
        return nodeyield[:potential_uitloop[0]], nodeyield[potential_uitloop[0]:]
    else:
        return nodeyield, []


def aanloopuitloopvu(stree: SynTree) -> List[SynTree]:
    results = []
    nodeyield = getnodeyield(stree)
    aanloop, remainder = get_aanloop_and_core(nodeyield)
    core, uitloop = getuitloop(remainder)
    topnode = find1(stree, './/node[@cat="top"]')
    if topnode is not None and len(aanloop) >= 2:
        topnodebegin = getattval(topnode, 'begin')
        vunode = aanloop[0]
        vunodebegin = getattval(vunode, 'begin')
        vunodelemma = getattval(vunode, 'lemma')
        if vunodebegin == topnodebegin and vunodelemma in vuwordslexicon:
            results.append(vunode)
    if len(uitloop) >= 2:
        vunode = uitloop[1]
        results.append(vunode)
    for node in core:
        nodelemma = getattval(node, 'lemma')
        if nodelemma in vuwordslexicon and '2' in vuwordslexicon[nodelemma]:
            results.append(node)
    return results


def only_puncs(nodelist: List[SynTree]) -> bool:
    for node in nodelist:
        nodelemma = getattval(node, 'lemma')
        if nodelemma not in punctuationchars:
            return False
    return True

potentialqwords = ['wat']
def firstwordispotentialqword(stree: SynTree) -> bool:
    nodeyield = getnodeyield(stree)
    firstnode = nodeyield[0] if nodeyield != [] else None
    if firstnode is None:
        return False
    else:
        firstnodelemma = gav(firstnode, 'lemma')
        result = firstnodelemma in potentialqwords
        return result

into_xpath = """.//node[@cat="top" and 
       (not(.//node[@pt="ww" and @wvorm!="pt"]) or not(.//node[@cat="sv1" and (@rel="--" or @rel="nucl" or @rel="dp")])) and 
       node[@lemma="?"] and 
       .//node[@pt!="let" and @pt != "tsw"] and
       not(.//node[@rel="tag" and @cat="sv1"]) and
       not(.//node[@cat="whq"]) and
       not(.//node[@pt="vnw" and (@vwtype="vrag" or @vwtype="vb")]) and
       not(.//node[@lemma="he" or @lemma="hè"]) and
       not(.//node[contains(@frame, "wh_adjective") or contains(@frame, "waar_adverb")]) and
       not(.//node[@lemma="huh"])

]

"""
def into(stree: SynTree) -> List[SynTree]:
    wordnodes = stree.xpath('.//node[@word]')
    wrongwordnodes = [wordnode for wordnode in wordnodes
                        if gav(wordnode, 'lemma').startswith('waar') and
                           is_pronominal_adverb(gav(wordnode,'lemma'))
                      ]
    if wrongwordnodes == []:
        rawintos = stree.xpath(into_xpath)
        result = [rawintos[0]] if rawintos != [] else []
    else:
        result = []
    if firstwordispotentialqword(stree):
        result = []
    return result

stamxpath = """.//node[@pt="ww" and @pvtijd="tgw" and
                       not(%verbal_VU%) and not(%Tarsp_Kop%) and
 not(%Tarsp_hww% or
     @lemma = "hebben" or
     @lemma = "worden" or
     @lemma = "zijn"   
  )
and @pvagr="ev"  ]"""
#  and not(parent::node[%basicimperative%]) eruit gehaald

expandedstamxpath = expandmacros(stamxpath)

def stam(stree: SynTree) -> List[SynTree]:
    results  = []
    coreresults = stree.xpath(expandedstamxpath)
    for result in coreresults:
        resultparent = result.getparent()
        imps = imperatives(resultparent)
        if imps == []:
            results.append(result)
    return results

bx_xpath = """.//node[%Tarsp_BX%]"""
expanded_bx_xpath = expandmacros(bx_xpath)

def bx(stree: SynTree) -> List[SynTree]:
    raw_bx_results = stree.xpath(expanded_bx_xpath)
    results = []
    for result in raw_bx_results:
        wxresults = wx(result)
        if wxresults == []:
            results.append(result)
    return results




rel_as_avn_xpath = """
.//node[@pt="vnw" and @rel="rhd" and 
        ../../../node[@cat="np" and @rel="--" and
                      node[@pt="n" and @rel="hd"] and
                      node[@cat="rel" and @rel="mod"]] and
	    ../node[@cat="ssub" and @rel="body" and
                node[@pt="ww" and @rel="hd"]]
      ]            """


def get_rel_as_avn_nodes(stree: SynTree) -> List[SynTree]:
    results = []
    rawnodes = stree.xpath(rel_as_avn_xpath)
    for rawnode in rawnodes:
        verbnodes = rawnode.xpath("""../node[@cat="ssub" and @rel="body" ]/node[@pt="ww" and @rel="hd"]""")
        if verbnodes != []:
            verbnode = verbnodes[0]
            if adjacent(rawnode, verbnode, stree):
                results.append(rawnode)
    return results

# this one rejected we prefer to transform the relevant structures
def get_avn(stree: SynTree) -> List[SynTree]:
    avn_xpath = expandmacros(""".//node[%AVn%]""")
    results = stree.xpath(avn_xpath)
    results += get_rel_as_avn_nodes(stree)
    return results

ov2_xpath = expandmacros(".//node[%Tarsp_ov2%]")
def ov2(stree: SynTree) -> List[SynTree]:
    """
    many more cases must be excluded, e.g. w(x), bv zn. die/dezezn etc, allow only two real words
    """
    bx_results = bx(stree)
    wx_results = wx(stree)
    if bx_results != [] or wx_results != []:
        return []
    results = stree.xpath(ov2_xpath)
    return results

zn_xpath = expandmacros(".//node[%Tarsp_Zn%]")

def tarsp_dellid(stree: SynTree) -> List[SynTree]:
    raw_results = get_missing_det(stree)
    zn_results = stree.xpath(zn_xpath)
    results = [result for result in raw_results if result not in zn_results]
    return results



def sublid(stree: SynTree) -> List[SynTree]:

    # deheterror
    deheterror_nodes = mdbasedquery(stree, correctionlabels.grammarerror, correctionlabels.deheterror)

    # hetdeerrors

    hetdeerror_nodes = mdbasedquery(stree, correctionlabels.grammarerror, correctionlabels.hetdeerror)

    other_nodes = sub_pt(stree, 'lid')
    results = deheterror_nodes + hetdeerror_nodes + other_nodes
    return results

def sub_pt(stree: SynTree, pt: str) -> List[SynTree]:
    """
    finds substitutions of words with part of speech == pt in stree
    It finds them on the basis of the metadata
    """
    results = []
    replacement_metadata = stree.xpath(mdnameonlyxpathtemplate.format(mdname=CHAT_replacement))
    explanation_as_replacement_metadata = (
        stree.xpath(mdnameonlyxpathtemplate.format(mdname=correctionlabels.explanationasreplacement)))
    all_metadata = replacement_metadata + explanation_as_replacement_metadata
    pt_replacement_metadata = []
    for replacement in all_metadata:
        annotated_list = eval(gav(replacement, 'annotatedwordlist'))
        annotation_list = eval(gav(replacement, 'annotationwordlist'))
        annotated = annotated_list[0] if annotated_list else None
        annotation = annotation_list[0] if annotation_list else None
        # if annotation in articles:    # this is not needed and may be wrong
                                        # if there are unexpected variants of articles
        #    pt_replacement_metadata.append(replacement)
        pt_replacement_metadata.append(replacement)
    for art_replacement in pt_replacement_metadata:
        new_node = get_node(stree, art_replacement, xpath_cond=f'@pt="{pt}"', annotation=True)
        if new_node is not None:
            results.append(new_node)
    return results


def stap_congruentiefout(stree: SynTree) -> List[SynTree]:
    results = congruentiefout(stree)

    delpv_results = asta_delpv(stree)

    results += delpv_results


    return results

def congruentiefout(stree: SynTree) -> List[SynTree]:
    errors, regionals, variants = congruentie_afwijkingen(stree)
    return errors

def pv_regionale_vorm(stree: SynTree) -> List[SynTree]:
    errors, regionals, variants = congruentie_afwijkingen(stree)
    return regionals

def congruentie_afwijkingen(stree: SynTree) -> Tuple[List[SynTree], List[SynTree], List[SynTree]]:
    errors = []
    regionals = []
    variants = []

    # part 1 based on CHAT-replacements
    replacement_metadata = stree.xpath(mdnameonlyxpathtemplate.format(mdname=CHAT_replacement))
    explanation_as_replacement_metadata = (
        stree.xpath(mdnameonlyxpathtemplate.format(mdname=correctionlabels.explanationasreplacement)))
    all_metadata = replacement_metadata + explanation_as_replacement_metadata
    for replacement in all_metadata:
        new_node = get_node(stree, replacement, xpath_cond=f'@pt="ww"', annotation=True)
        annotated = get_word(replacement, 'annotatedwordlist')
        annotation = get_word(replacement, 'annotationwordlist')
        if new_node is not None:
            if (annotated, annotation) in regional_pv_variants:
                regionals.append(new_node)
                continue
            if (annotated, annotation) in regular_pv_variants:
                variants.append(new_node)
                continue
            # determine the grammatical properties of annotated if it is a real word
            if informlexicon(annotated):
                annotated_word_infos = getwordposinfo(annotated, pos='ww')
                annotation_word_infos = getwordposinfo(annotation, pos='ww')
                for annotated_word_info in annotated_word_infos:
                    # determine its lemma, check if it is the same as the lemma for the annotation
                    annotated_lemma = annotated_word_info[3]
                    for annotation_word_info in annotation_word_infos:
                        annotation_lemma =annotation_word_info[3]
                        if annotated_lemma == annotation_lemma:
                            # check whether the grammatical properties only differ in pvagr
                            annotated_celex_infl = annotated_word_info[2]
                            annotation_celex_infl = annotation_word_info[2]
                            if annotated_celex_infl in celex2dcoimap and annotation_celex_infl in celex2dcoimap:
                               annotated_infl = celex2dcoimap[annotated_celex_infl]
                               annotation_infl = celex2dcoimap[annotation_celex_infl]
                               ok = annotation_infl['wvorm'] == annotated_infl['wvorm'] and \
                                    annotation_infl['pvtijd'] == annotated_infl['pvtijd'] and \
                                    annotation_infl['pvagr'] != annotated_infl['pvagr']
                            else:
                                ok = False
                                settings.LOGGER.error(f'Missing value in celex2dcoimap: {annotated_celex_infl}.')
                            if ok:

                                errors.append(new_node)
                                break

    # part 2: svaerrors
    sva_error_metadata = stree.xpath(sva_error_xpath)
    for sva_error_meta in sva_error_metadata:
        new_node = get_node(stree, sva_error_meta)
        annotated = get_word(sva_error_meta, 'annotatedwordlist')
        annotation = get_word(sva_error_meta, 'annotationwordlist')

        if (annotated, annotation) in regional_pv_variants:
            regionals.append(new_node)
            continue
        if (annotated, annotation) in regular_pv_variants:
            variants.append(new_node)
            continue
        if new_node is not None:
            errors.append(new_node)


    # we do not want duplicate nodes
    errors = list(set(errors))
    regionals = list(set(regionals))
    variants = list(set(variants))

    return errors, regionals, variants




def vt_fout(stree: SynTree) -> List[SynTree]:
    overgen_nodes = get_overgeneralisations(stree)
    replacement_nodes = get_replacement_nodes(stree)
    wrong_nodes = overgen_nodes + replacement_nodes
    results = [node for node in wrong_nodes if gav(node, 'wvorm') == 'pv' and gav(node, 'pvtijd') == 'verl']
    return results

def vd_fout(stree: SynTree) -> List[SynTree]:
    morph_error_nodes = get_morphological_errors(stree)
    replacement_nodes = get_replacement_nodes(stree)
    wrong_nodes = morph_error_nodes + replacement_nodes
    results = [node for node in wrong_nodes if gav(node, 'wvorm') == 'vd' ]
    return results


def get_replacement_metadata(stree: SynTree) -> List[SynTree]:
    replacement_metadata = stree.xpath(mdnameonlyxpathtemplate.format(mdname=CHAT_replacement))
    explanation_as_replacement_metadata = (
        stree.xpath(mdnameonlyxpathtemplate.format(mdname=correctionlabels.explanationasreplacement)))
    noncompletion_metadata = stree.xpath(mdnameonlyxpathtemplate.format(mdname=CHAT_wordnoncompletion))
    all_metadata = replacement_metadata + explanation_as_replacement_metadata + noncompletion_metadata
    return all_metadata


def get_replacement_nodes(stree: SynTree) -> List[SynTree]:
    all_metadata = get_replacement_metadata(stree)
    raw_result = [get_node(stree, meta, annotation=True) for meta in all_metadata]
    result = [node for node in raw_result if node is not None]
    return result



def get_morphological_errors(stree: SynTree) -> List[SynTree]:
    errors = []
    morph_error_metadata = stree.xpath(morph_error_xpath)
    for morph_error_meta in morph_error_metadata:
        new_node = get_node(stree, morph_error_meta)
        if new_node is not None:
            errors.append(new_node)

    errors = list(set(errors))
    return errors


def get_overgeneralisations(stree: SynTree) -> List[SynTree]:
    errors = []

    # based on corrections by SASTA
    infl_error_metadata = stree.xpath(infl_error_xpath)
    for infl_error_meta in infl_error_metadata:
        new_node = get_node(stree, infl_error_meta)
        # annotated = get_word(stree, infl_error_meta, 'annotatedwordlist')
        # annotation = get_word(stree, infl_error_meta, 'annotationwordlist')

        if new_node is not None:
            errors.append(new_node)

    # we do not want duplicate nodes
    errors = list(set(errors))

    return errors


def get_overgeneralisation_replacement_nodes(stree: SynTree) -> List[SynTree]:
    errors = []

    # based on CHAT-replacements
    all_metadata = get_replacement_metadata(stree)
    for replacement in all_metadata:
        annotated = get_word(replacement, 'annotatedwordlist')
        annotation = get_word(replacement, 'annotationwordlist')
        corrected_inflections = []
        if not informlexicon(annotated):
            raw_corrected_inflections = correctinflection(annotated)
            corrected_inflections = [ci for ci in raw_corrected_inflections if ci[0] == annotation]
        if corrected_inflections != []:
            new_node = get_node(stree, replacement, xpath_cond='', annotation=True)
            errors.append(new_node)

    # no duplicates
    errors = list(set(errors))
    return errors













