"""
scratch file to add new functions while the system is running so we do not want to change files that are in use
"""
from lxml import etree
import copy
from sastadev import correctionlabels
from sastadev.basicreplacements import wrongmorph, ervzvariants, basicreplacements
from sastadev.CHAT_Annotation import CHAT_replacement, CHAT_omittedword, CHAT_retracing
from sastadev.celexlexicon import celex2dcoimap
from sastadev.conf import settings
from sastadev.constants import false_start_mode, repetition_mode, self_correction_mode
from sastadev.deregularise import correctinflection, overgen, wrongovergen
from sastadev.filefunctions import get_corrected_tree_fullname
from sastadev.iedims import getjeforms
from sastadev.find_ngram import findmatches, is_def_det, ngram21
from sastadev.lexicon import getwordinfo, getwordposinfo, filledpauseslexicon, informlexicon
from sastadev.macros import expandmacros
from sastadev.metadata import Meta, bpl_delete, mkinsertmeta, mkSASTAMeta, defaultpenalty
from sastadev.missing_det import get_missing_det
from sastadev.normalise_lemma import normaliselemma
from sastadev.queryfunctions import get_replacement_metadata
from sastadev.sastatypes import Relation, SynTree, TreeBank, UttId
from sastadev.sastatoken import Token
from sastadev.smallclauses import mkinsertmeta, realword, word
from sastadev.test_functions import test_f, get_stree, test_transform_f
from sastadev.tokenmd import TokenListMD
from sastadev.treebankfunctions import (find1, getattval, get_node, getnodeyield, getorigutt, getsentence,
                                        getxsid, getuttid, get_word,
                                        mktoken2nodemap, mdbasedquery,
                                        mdnameonlyxpathtemplate)
from typing import Callable, List, Optional, Tuple

gav = getattval



def sub_tijd(stree: SynTree) -> List[SynTree]:
    results = []
    replacement_metadata = get_replacement_metadata(stree)
    for replacement_meta in replacement_metadata:
        annotated_list = eval(gav(replacement_meta, 'annotatedwordlist'))
        annotation_list = eval(gav(replacement_meta, 'annotationwordlist'))
        if len(annotation_list) > 1:
            continue
        annotated = annotated_list[0]
        if not informlexicon(annotated):
            continue
        annotation = annotation_list[0]
        annotated_node = get_node(stree, replacement_meta, annotation=True)
        annotated_pt = gav(annotated_node, 'pt')
        if annotated_pt != 'ww':
            continue
        annotated_pvtijd = gav(annotated_node, 'pvtijd')
        annotation_wordinfos = getwordposinfo(annotation, annotated_pt)
        for annotation_wordinfo in annotation_wordinfos:
            infl = annotation_wordinfo[2]
            annotation_featdict = celex2dcoimap[infl] if infl in celex2dcoimap else {}
            annotation_pvtijd = annotation_featdict['pvtijd'] if 'pvtijd' in annotation_featdict else ''
            if annotation_wordinfo[0] == annotated_pt and \
                annotation_pvtijd != '' and \
                annotated_pvtijd != '' and \
                annotation_pvtijd != annotated_pvtijd:
                results.append(annotated_node)
                break
    return results

lexical_error_pts = ['n', 'adj', 'ww']
def lexical_error(stree: SynTree) -> List[SynTree]:
    results = []
    replacement_metadata = get_replacement_metadata(stree)
    for replacement_meta in replacement_metadata:
        annotated_list = eval(gav(replacement_meta, 'annotatedwordlist'))
        annotation_list = eval(gav(replacement_meta, 'annotationwordlist'))
        annotated = annotated_list[0]
        if not informlexicon(annotated):
            continue
        annotation = annotation_list[0]
        annotated_node = get_node(stree, replacement_meta, annotation=True)
        annotated_pt = gav(annotated_node, 'pt')
        annotated_lemma = gav(annotated_node, 'original_lemma')
        annotation_lemma = gav(annotated_node, 'lemma')
        if annotated_lemma != '' and annotated_lemma != annotation_lemma and annotated_pt in lexical_error_pts:
            results.append(annotated_node)
    return results


lexical_error_triples = [('test_stap', 'test_stap', '16'),
           ('vklstap', 'STAP_04', '26'),
           ('vklstap', 'STAP_08', '31'),
           ('vklstap', 'STAP_07', '29'),
           ('vklstapfase2', 'STAP_024', '16'),
           ]

sub_tijd_triples = [ ('test_stap', 'test_stap', '11'),
                    ('vklstap', 'STAP_02', '11'),
                    ('vklstap', 'STAP_02', '17'),
                    ('vklstap', 'STAP_02', '34'),
                    ('vklstap', 'STAP_02', '47'),
                    ('vklstap', 'STAP_02', '48'),
                    ('vklstap', 'STAP_02', '47'),
                    ('vklstap', 'STAP_08', '3'),
                    ('vklstap', 'STAP_09', '41')]




main_with_als_xpath = './/node[@cat="smain" and node[@rel="mod" and @cat="cp" and node[@rel="cmp" and @lemma="als"]]]'
def transform_als_dan(in_stree: SynTree) -> SynTree:
    stree = copy.deepcopy(in_stree)
    als_dan_clauses = stree.xpath(main_with_als_xpath)

    for als_dan_clause in als_dan_clauses:
        cp_node = find1(als_dan_clause, './node[@rel="mod" and @cat="cp" and node[@rel="cmp" and @lemma="als"]]')
        cp_nodes = getnodeyield(cp_node)
        if cp_nodes != [] and gav(cp_nodes[-1], 'lemma') == 'dan':
            dan_node = cp_nodes[-1]
            dan_parent = dan_node.getparent()
            dan_parent.remove(dan_node)
            als_dan_clause.append(dan_node)
    return stree

als_dan_triples = [('vklstap', 'stap_04', '44'),
('vklstap', 'stap_05', '25'),
('vklstap', 'stap_05', '26'),
('vklstap', 'stap_08', '31'),
('vkltarsp', 'tarsp_07', '24'),
('handreiking4-12', 'handreiking4-12', '73'),
('handreiking4-12', 'handreiking4-12', '95'),
('handreiking4-12', 'handreiking4-12', '118'),
]

dependent_verb_xpath = ('../node[@rel="vc" and (@cat="inf" or @cat="ppart")]/node[@rel="hd" and @pt="ww"] |'
                        '../node[@rel="vc" and (@cat="ti"]/node[@cat="inf"]/node[@rel="hd" and @pt="ww"]')
def get_ww_dependent_verbs(ww: SynTree) -> List[SynTree]:
    dependent_verbs = ww.xpath(dependent_verb_xpath)
    results = dependent_verbs
    for dependent_verb in dependent_verbs:
        rec_dependent_verbs = get_ww_dependent_verbs(dependent_verb)
        results += rec_dependent_verbs
    return results

def get_retracing_word_count(stree: SynTree, mode=None) -> int:
    result = 0
    retracings = stree.xpath(f'.//xmeta[@name="{CHAT_retracing}"]')
    cleanedtokenpositions_meta = find1(stree, './/xmeta[@name="cleanedtokenpositions"]')
    cleanedtokenisation = find1(stree, './/xmeta[@name="cleanedtokenisation"]')
    if cleanedtokenpositions_meta is not None:
        cleanedtokens_annotationposlist = eval(gav(cleanedtokenpositions_meta, 'annotationposlist'))
        cleanedtokens_wordlist = eval(gav(cleanedtokenisation, 'annotationwordlist'))
        for retracing in retracings:
            retracing_annotationposlist = eval(gav(retracing, 'annotationposlist'))
            if mode is false_start_mode:
                cond = is_false_start(retracing, cleanedtokenisation, cleanedtokenpositions_meta)
            elif mode == self_correction_mode:
                cond = is_self_correction(retracing, cleanedtokenisation, cleanedtokenpositions_meta)
            elif mode == repetition_mode:
                cond = is_repetition_retracing(retracing, cleanedtokenisation, cleanedtokenpositions_meta)
            else:
                cond = True
            if cond:
                result += len(retracing_annotationposlist)
    return result

def get_tb_false_start_word_counts(tb: TreeBank) -> List[Tuple[UttId, int]]:
    results = []
    for stree in tb:
        xsid = getxsid(stree)
        fs_count = get_retracing_word_count(stree, mode=false_start_mode)
        results.append((xsid, fs_count))
    return results



def is_false_start(retracing, cleanedtokenisation, cleanedtokenpositions_meta) -> bool:
    retracing_annotationposlist = eval(gav(retracing, 'annotationposlist'))
    cleanedtokens_annotationposlist = eval(gav(cleanedtokenpositions_meta, 'annotationposlist'))
    result = (cleanedtokens_annotationposlist != [] and retracing_annotationposlist != [] and
            not (cleanedtokens_annotationposlist[0] < retracing_annotationposlist[0]) and
            not is_repetition_retracing(retracing, cleanedtokenisation, cleanedtokenpositions_meta))
    return result

def is_self_correction(retracing, cleanedtokenisation, cleanedtokenpositions_meta) -> bool:
    retracing_annotationposlist = eval(gav(retracing, 'annotationposlist'))
    cleanedtokens_annotationposlist = eval(gav(cleanedtokenpositions_meta, 'annotationposlist'))
    result = (cleanedtokens_annotationposlist != [] and retracing_annotationposlist != [] and
                cleanedtokens_annotationposlist[0] < retracing_annotationposlist[0] and
                not is_repetition_retracing(retracing, cleanedtokenisation, cleanedtokenpositions_meta))
    return result

def is_repetition(retracing, cleanedtokenisation, cleanedtokenpositions_meta) -> bool:
    retracing_annotationposlist = eval(gav(retracing, 'annotationposlist'))
    cleanedtokens_annotationposlist = eval(gav(cleanedtokenpositions_meta, 'annotationposlist'))
    result = (cleanedtokens_annotationposlist != [] and retracing_annotationposlist != [] and
            not (cleanedtokens_annotationposlist[0] < retracing_annotationposlist[0]) and
            not is_repetition_retracing(retracing, cleanedtokenisation, cleanedtokenpositions_meta))
    return result



def is_repetition_retracing(retracing, cleanedtokenisation, cleanedtokenpositions_meta) -> bool:
    return False

if __name__ == '__main__':
    pass
    # test_f(lexical_error_triples, lexical_error)
    # sub_tijd_triples = [sub_tijd_triples[0], sub_tijd_triples[7]]
    # test_f(sub_tijd_triples, sub_tijd)
    test_transform_f(als_dan_triples, transform_als_dan)

