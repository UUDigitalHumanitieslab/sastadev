from sastadev import correctionlabels
from sastadev.allresults import AllResults
from sastadev.CHAT_Annotation import CHAT_wordnoncompletion, CHAT_replacement
from sastadev.deregularise import detailed_detect_error
from sastadev.metadata import bpl_none, Meta, mkSASTAMeta
from sastadev.predcvagreement import get_predc_v_mismatches
from sastadev.sastatypes import SynTree, TreeBank
from sastadev.treebankfunctions import add_metadata, find1, getattval as gav, getnodeyield
from typing import List, Optional

replacementxpath = f""".//xmeta[@name="{correctionlabels.replacement}" or 
                                @name="{CHAT_replacement}" or 
                                @name="{CHAT_wordnoncompletion}" or 
                                @name="{correctionlabels.noncompletion}" or 
                                @name="{correctionlabels.explanationasreplacement}" 
                               ]"""
sasta = 'SASTA'

# Meta(name, value, annotationwordlist=[], annotationposlist=[], annotatedposlist=[],
#                  annotatedwordlist=[], annotationcharlist=[
#     ], annotationcharposlist=[], annotatedcharlist=[],
#             annotatedcharposlist=[], atype='text', cat=None, subcat=None, source=None, penalty=defaultpenalty,
#             backplacement=defaultbackplacement)

def get_meta_attr(meta: SynTree, attr: str) -> Optional[str]:
    wordliststr = gav(meta, attr)
    wordlist = eval(wordliststr)
    result = wordlist[0] if wordlist != [] else None
    return result



def find_grammar_errors_in_allresults(allresults: AllResults) -> AllResults:
    strees = allresults.analysedtrees
    newstrees = []
    for xsid, stree in strees:
        metalist = find_grammar_errors_in_stree(stree)
        if metalist == []:
            newstree = stree
        else:
            newstree = add_metadata(stree, metalist)
        newstrees.append((xsid, newstree))
    allresults.analysedtrees = newstrees                    # warning this modifies the input allresults
    return allresults

def find_grammar_errors_in_stree(stree: SynTree) -> List[Meta]:
    results = []
    matches = get_predc_v_mismatches(stree)
    for match in matches:
        verb = find1(match, './node[@rel="hd"]')
        thenodeyield = getnodeyield(match)
        annotatedwordlist = [gav(nd, 'word') for nd in thenodeyield]
        annotatedposlist = [gav(nd, 'end') for nd in thenodeyield]
        if verb is not None:
            meta = Meta(name=correctionlabels.agreementerror,
                        value=correctionlabels.predc_v_agreement_error,
                        cat=correctionlabels.syntax,
                        annotatedposlist=annotatedposlist, annotatedwordlist=annotatedwordlist,
                        subcat=None, source=sasta, backplacement=bpl_none)
            results.append(meta)
    matches = stree.xpath(replacementxpath)
    for match in matches:
        word = get_meta_attr(match, 'annotatedwordlist')
        correction = get_meta_attr(match, 'annotationwordlist')
        wordposition = get_meta_attr(match, 'annotatedposlist')
        if word is not None and correction is not None:
            errorfound, errormsg = detailed_detect_error(word, correction)
            if errorfound:
                annotatedwordlist = [word]
                annotatedposlist = [wordposition]
                meta = Meta(name=correctionlabels.morphologicalerror, value=errormsg,
                            cat=correctionlabels.morphology, annotationwordlist=[correction],
                            annotationposlist=annotatedposlist,
                            annotatedposlist=annotatedposlist, annotatedwordlist=annotatedwordlist,
                            subcat=None, source=sasta, backplacement=bpl_none)
                results.append(meta)
    return results






