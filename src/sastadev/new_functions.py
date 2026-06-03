"""
scratch file to add new functions while the system is running so we do not want to change files that are in use
"""
from sastadev import correctionlabels
from sastadev.CHAT_Annotation import CHAT_replacement
from sastadev.celexlexicon import celex2dcoimap
from sastadev.conf import settings
from sastadev.deregularise import correctinflection, overgen, wrongovergen
from sastadev.lexicon import getwordposinfo, informlexicon
from sastadev.macros import expandmacros
from sastadev.metadata import Meta
from sastadev.missing_det import get_missing_det
from sastadev.sastatypes import SynTree
from sastadev.sastatoken import Token

from sastadev.treebankfunctions import getattval, get_node, getnodeyield, get_word, mdnameonlyxpathtemplate
from typing import List

gav = getattval

infl_error_xpath = f""".//xmeta[@name="{correctionlabels.morphologicalerror}" and 
                                (@value="{overgen}" or @value="{wrongovergen}")]"""


def vt_fout(stree: SynTree) -> List[SynTree]:
    overgen_nodes = get_overgeneralisations(stree)
    replacement_nodes = get_replacement_nodes(stree)
    wrong_nodes = overgen_nodes + replacement_nodes
    results = [node for node in wrong_nodes if gav(node, 'wvorm') == 'pv' and gav(node, 'pvtijd') == 'verl']
    return results


def get_replacement_metadata(stree: SynTree) -> List[Meta]:
    replacement_metadata = stree.xpath(mdnameonlyxpathtemplate.format(mdname=CHAT_replacement))
    explanation_as_replacement_metadata = (
        stree.xpath(mdnameonlyxpathtemplate.format(mdname=correctionlabels.explanationasreplacement)))
    all_metadata = replacement_metadata + explanation_as_replacement_metadata
    return all_metadata


def get_replacement_nodes(stree: SynTree) -> List[SynTree]:
    all_metadata = get_replacement_metadata(stree)
    result = [get_node(meta) for meta in all_metadata]
    return result

def get_overgeneralisations(stree: SynTree) -> List[SynTree]:
    errors = []

    # based on corrections by SASTA
    infl_error_metadata = stree.xpath(infl_error_xpath)
    for infl_error_meta in infl_error_metadata:
        new_node = get_node(stree, infl_error_meta)
        # annotated = get_word(infl_error_meta, 'annotatedwordlist')
        # annotation = get_word(infl_error_meta, 'annotationwordlist')

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

